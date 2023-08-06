#######################################################################
#
# Copyright (C) 2022 David Palao
#
# This file is part of PacBioDataProcessing.
#
#  PacBioDataProcessing is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PacBio data processing is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with PacBioDataProcessing. If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

from collections.abc import Iterable
import re
from datetime import datetime, timedelta
import socket
from concurrent.futures import ThreadPoolExecutor
from functools import cached_property
from hashlib import md5
import imghdr
import time
from pathlib import Path
import os
import subprocess as sp

import pyfaidx

from pacbio_data_processing import __version__ as VERSION
from pacbio_data_processing.bam import BamFile

from .utils import (
    SummaryReportParser, run_sm_analysis, normalize_whitespaces,
    count_marker_files,
)


SM_ANALYSIS_IMAGES = {
    "molecule_type_bars": "figures/{prefix}molecule_type_bars.png",
    "molecule_len_histogram": "figures/{prefix}molecule_length_histogram.png",
    "position_coverage_bars": "figures/{prefix}position_coverage_bars.png",
    "position_coverage_history": (
        "figures/{prefix}position_coverage_history.png"),
    "gatc_coverage_bars": "figures/{prefix}gatc_coverage_bars.png",
    "meth_type_bars": "figures/{prefix}meth_type_bars.png",
}
MISSING_CCS_MSG = (
    "Aligned CCS file cannot be produced without CCS "
    "file. Trying to produce it..."
)


class SmAnalysisMixIn:
    def collect_opts_for_tests(self, sm_test_data):
        # Should clos be a list or a tuple?
        self.clos = sm_test_data["CLOs"]
        self.bam = sm_test_data["bam"]
        self.statistics_of_test_fixture = sm_test_data["statistics"]
        self.aligned_bam = sm_test_data.get("aligned bam")
        self.pi_shifted_aligned_bam = sm_test_data.get(
            "pi-shifted aligned bam")
        self.fasta = sm_test_data["fasta"]
        self.pi_shifted_fasta = self.fasta.with_name(
            "pi-shifted."+self.fasta.name)
        self.expected_gff = sm_test_data["gff"]
        self.expected_csv = sm_test_data["csv"]
        self.expected_meth_report = sm_test_data["methylation-report"]
        self.imperfect_molecules = sm_test_data[
            "mol ids with reference mismatch"]
        self.rejected_molecules = sm_test_data["mols rejected by filters"]
        self.all_molecules = sm_test_data["molecules"]
        self.one_mol_bams = [
            str(self.bam).replace(
                ".bam", f".{m}.bam") for m in self.all_molecules
            if m not in self.imperfect_molecules
        ]
        self.analyzed_molecules = (
            set(self.all_molecules)
            - set(self.rejected_molecules)
            - set(self.imperfect_molecules)
        )
        self.num_ccs_mols = sm_test_data["num CCS molecules"]
        self.unaligned_input = ("unaligned input" in sm_test_data["features"])
        self.faulty_molecules = {
            _: {} for _ in sm_test_data.get("faulty molecules", ())
        }

    @cached_property
    def executor(self) -> ThreadPoolExecutor:
        """Just in case it is needed, an executor can be created."""
        return ThreadPoolExecutor(max_workers=2)

    def make_ccs(self, missing_ok=False):
        """It calls the ccs program and deletes the marker file possibly
        created by the fake ccs tools.
        """
        proc = sp.Popen(
            ["ccs", self.bam, self.ccs], stdout=sp.PIPE, stderr=sp.PIPE
        )
        marker = Path(f".ccs.pid.{proc.pid}")
        while True:
            try:
                marker.unlink(missing_ok)
            except OSError:
                files = os.listdir()
                print("cwd:", os.getcwd())
                print(f"  trying to remove: {marker}")
                print(f"   dir contents ({len(files)} files):", files)
                time.sleep(1)
            else:
                break

    @cached_property
    def ccs(self):
        """It returns the Path corresponding to the *canonical* ccs
        file constructed from ``self.bam``."""
        ccs_name = "ccs."+self.bam.name
        return self.bam.with_name(ccs_name)

    @cached_property
    def blasr_ccs(self):
        blasr_ccs_name = "blasr."+self.ccs.name
        return self.ccs.with_name(blasr_ccs_name)

    @cached_property
    def pi_shifted_blasr_ccs(self):
        pi_shifted_blasr_ccs_name = "pi-shifted.blasr."+self.ccs.name
        return self.ccs.with_name(pi_shifted_blasr_ccs_name)

    @cached_property
    def blasr_bam(self):
        blasr_name = "blasr."+self.bam.name
        return self.bam.with_name(blasr_name)

    @cached_property
    def pi_shifted_blasr_bam(self):
        pi_shifted_blasr_name = "pi-shifted.blasr."+self.bam.name
        return self.bam.with_name(pi_shifted_blasr_name)

    @property
    def partition_prefix(self):
        partition_prefix = ""
        for arg in ("-P", "--partition"):
            if arg in self.clos:
                partition, partitions = (
                    self.clos[self.clos.index(arg)+1].split(":")
                )
                partition_prefix = f"partition_{partition}of{partitions}."
        return partition_prefix

    @property
    def found_meth_report(self):
        return self.bam.with_name(
            "methylation."+self.partition_prefix+"sm-analysis."
            + self.bam.stem+".csv"
        )

    @property
    def found_summary_report(self):
        return self.bam.with_name(
            "summary."+self.partition_prefix+"sm-analysis."
            + self.bam.stem+".html"
        )

    @property
    def found_csv(self):
        return self.bam.with_name(
            self.partition_prefix+"sm-analysis."+self.bam.stem+".csv"
        )

    @property
    def found_gff(self):
        return self.bam.with_name(
            self.partition_prefix+"sm-analysis."+self.bam.stem+".gff"
        )

    def check_temp_files(
            self, output, one_mol_bams, rejected_molecules, options):
        """Aux method: checks temp files backup related messages and looks
        for temp files.
        """
        assert "keep temp dir: yes" in output
        if "--verbose" in options:
            assert re.search(
                r"Copied temporary dir to: 'tmp[\w]+.backup'",
                output) is not None
        rootg = Path(".").iterdir()
        tempdirs = {
            x for x in rootg if x.is_dir() and x.name.startswith("tmp")}
        tempfiles = set()
        for d in tempdirs:
            tempfiles.update({_ for _ in d.iterdir()})
        for one_mol_bam in one_mol_bams:
            rejected = any(
                _ in one_mol_bam for _ in rejected_molecules)
            assert any(i.match(f"tmp*/{one_mol_bam}") for i in tempfiles)
            if not rejected:
                assert any(
                    i.match(f"tmp*/{one_mol_bam}.pbi") for i in tempfiles
                )

    def check_modification_types(self, output, options):
        mod_types = ['m6A']
        for arg in ("-m", "--modification-types"):
            if arg in options:
                mod_types = []
                # very basic parsing of clos:
                idx = options.index(arg)+1
                for mod_type in options[idx:]:
                    if mod_type.startswith("-"):
                        break
                    else:
                        mod_types.append(mod_type)
        assert f"modification types: {mod_types}" in output
        for mod_type in mod_types:
            if mod_type != "m6A":
                ignore_msg = (
                    f"[methylation report] modifications of type '{mod_type}'"
                    " will be ignored"
                )
                assert ignore_msg in output

    def check_for_gff(self):
        """Auxiliary method to directly check that the gff file is correct."""
        with open(self.found_gff) as gff_f:
            with open(self.expected_gff) as expected_gff_f:
                expected_gff_lines = [
                    _ for _ in expected_gff_f.readlines() if
                    not _.startswith("#")
                ]
                gff_lines = [
                    _ for _ in gff_f.readlines() if not _.startswith("#")
                ]
                assert expected_gff_lines == gff_lines

    def check_for_csv(self, output):
        with open(self.found_csv) as csv_f:
            with open(self.expected_csv) as expected_csv_f:
                assert expected_csv_f.read() == csv_f.read()
        own_output_message = f"Own output '{self.found_csv}' created"
        assert own_output_message in output

    def check_ipdsummary_program_and_processes(
            self, options, output, cmd_result):
        ipdSummary = "ipdSummary"
        for arg in ("-i", "--ipdsummary-path"):
            if arg in options:
                ipdSummary = options[options.index(arg)+1]
                break
        assert f"ipd program: '{ipdSummary}'" in output

        ipdsummary_instances = 1
        for arg in ("-N", "--num-simultaneous-ipdsummarys"):
            if arg in options:
                ipdsummary_instances = int(options[options.index(arg)+1])
                break
        assert f"# ipd program instances: {ipdsummary_instances}" in output

        ipdsummary_workers = 1
        for arg in ("-n", "--num-workers-per-ipdsummary"):
            if arg in options:
                ipdsummary_workers = int(options[options.index(arg)+1])
                break
        assert f"# workers per ipd instance: {ipdsummary_workers}" in output
        # (the following is because if num workers > 1, then the processes
        #  are the workers plus 1 times the number of ipdsummary instances)
        # The expression is:
        #  total #procs = #mols*(1+workers) = #mols + #mols*workers
        num_healthy_mols = len(self.analyzed_molecules)
        expected_ipdsummary_processes = num_healthy_mols*ipdsummary_workers
        if "--only-produce-methylation-report" not in options:
            assert (
                expected_ipdsummary_processes
                == count_marker_files("ipdSummary")
            )

    def check_one_molecule_bam_files_produced(self, output, options):
        if "--only-produce-methylation-report" not in options:
            for one_mol_file in self.one_mol_bams:
                if self.unaligned_input:
                    prefixes = ["blasr.", "pi-shifted.blasr."]
                else:
                    prefixes = [""]
                matches = []
                for pref in prefixes:
                    one_mol_bam_produced_msg = (
                        f"One-molecule BAM file written: \\w+/{pref}"
                        f"{one_mol_file}"
                    )
                    matches.append(re.search(one_mol_bam_produced_msg, output))
                assert any(matches), one_mol_bam_produced_msg

    def make_expected_summary_report(self, clos):
        stats = self.statistics_of_test_fixture
        methylation_report = self.found_meth_report
        raw_detections = self.found_csv
        gff_results = self.found_gff
        h1 = "Summary report: Single Molecule Methylation Analysis"
        overview_head = h1 + " >> " + "Overview"
        results_head = h1 + " >> " + "Result filenames"
        inputs_head = h1 + " >> " + "Input files"
        bam_file_head = inputs_head + " >> " + "BAM File"
        reference_file_head = inputs_head + " >> " + "Reference"
        mols_subs_head = h1 + " >> " + "Molecules/subreads"
        seq_coverage_head = h1 + " >> " + "Sequencing Position Coverage"
        GATCs_head = h1 + " >> " + "GATCs"
        methylations_head = GATCs_head + " >> " + "Methylations"

        # There exists an HTML file containing a summary of the process...
        overview_dict = {
            "PacBio Data Processing version": VERSION,
            "Date": datetime.now().isoformat(timespec="minutes"),
            "Program name": "sm-analysis",
            "Program options": " ".join(
                [str(self.bam), str(self.fasta)]+list(clos)),
            "Hostname": socket.gethostname(),
        }
        # ...a summary with result files...
        results_dict = {
            "Methylation report": f"{methylation_report}",
            "Raw detections": f"{raw_detections}",
            "Joint ": f"{gff_results}",
        }
        bamfile = BamFile(self.bam)
        # ...some info about the input BAM...
        bam_dict = {
            "File name": str(self.bam),
            "Size (bytes)": str(self.bam.stat().st_size),
            "MD5 checksum (full)": md5(open(self.bam, "rb").read()
                                       ).hexdigest(),
            "MD5 checksum (body)": bamfile.md5sum_body,
        }
        # ...as well as info about the input fasta...
        genes = pyfaidx.Fasta(str(self.fasta))
        gene = genes[0]
        reference_base_pairs = len(gene)
        reference_dict = {
            "File name": str(self.fasta),
            "Reference name": gene.long_name.strip(),
            "Size (base pairs)": str(reference_base_pairs),
            "MD5 checksum (fully capitalized string)": md5(
                str(gene).upper().encode("utf8")
            ).hexdigest(),
        }
        # ...statistics about the molecules and subreads...
        molecules_subreads_dict = {
            "Initial": {
                "number of molecules": "{mols_ini}".format(**stats),
                "number of subreads": "{subreads_ini}".format(**stats),
            },
            "Used in aligned CCS BAM": {
                "number of molecules": (
                    "{mols_used_in_aligned_ccs} "
                    "({perc_mols_used_in_aligned_ccs} %)"
                ).format(**stats),
                "number of subreads": (
                    "{subreads_used_in_aligned_ccs} "
                    "({perc_subreads_used_in_aligned_ccs} %)"
                ).format(**stats),
            },
            "DNA mismatch discards": {
                "number of molecules": (
                    "{mols_dna_mismatches} ({perc_mols_dna_mismatches} %)"
                ).format(**stats),
                "number of subreads": (
                    "{subreads_dna_mismatches} "
                    "({perc_subreads_dna_mismatches} %)"
                ).format(**stats),
            },
            "Filtered out": {
                "number of molecules": (
                    "{filtered_out_mols} ({perc_filtered_out_mols} %)"
                ).format(**stats),
                "number of subreads": (
                    "{filtered_out_subreads} ({perc_filtered_out_subreads} %)"
                ).format(**stats),
            },
            "Faulty (with processing error)": {
                "number of molecules": (
                    "{faulty_mols} ({perc_faulty_mols} %)"
                ).format(**stats),
                "number of subreads": (
                    "{faulty_subreads} ({perc_faulty_subreads} %)"
                ).format(**stats),
            },
            "In methylation report...": {
                "number of molecules": (
                    "{mols_in_meth_report} ({perc_mols_in_meth_report} %)"
                ).format(**stats),
                "number of subreads": (
                    "{subreads_in_meth_report} "
                    "({perc_subreads_in_meth_report} %)"
                ).format(**stats),
            },
            "...only with GATCs": {
                "number of molecules": (
                    "{mols_in_meth_report_with_gatcs} "
                    "({perc_mols_in_meth_report_with_gatcs} %)"
                ).format(**stats),
                "number of subreads": (
                    "{subreads_in_meth_report_with_gatcs} "
                    "({perc_subreads_in_meth_report_with_gatcs} %)"
                ).format(**stats),
            },
            "...only without GATCs": {
                "number of molecules": (
                    "{mols_in_meth_report_without_gatcs} "
                    "({perc_mols_in_meth_report_without_gatcs} %)"
                ).format(**stats),
                "number of subreads": (
                    "{subreads_in_meth_report_without_gatcs} "
                    "({perc_subreads_in_meth_report_without_gatcs} %)"
                ).format(**stats),
            },
        }

        # ...statistics about the coverage...
        seq_coverage_dict = {
            "Number of base pairs in reference": (
                f"{reference_base_pairs}"
            ),
            "Positions covered by molecules in the BAM file": (
                "{all_positions_in_bam} ({perc_all_positions_in_bam} %)"
            ).format(**stats),
            "Positions NOT covered by molecules in the BAM file": (
                "{all_positions_not_in_bam} "
                "({perc_all_positions_not_in_bam} %)"
            ).format(**stats),
            "Positions covered by molecules in the methylation report": (
                "{all_positions_in_meth} ({perc_all_positions_in_meth} %)"
            ).format(**stats),
            "Positions NOT covered by molecules in the methylation report": (
                "{all_positions_not_in_meth} "
                "({perc_all_positions_not_in_meth} %)"
            ).format(**stats),
        }

        # ...about the GATCs...
        GATCs_dict = {
            "Total number of GATCs in reference": (
                "{total_gatcs_in_ref}"
            ).format(**stats),
            "Number of GATCs identified in the BAM file": (
                "{all_gatcs_identified_in_bam} "
                "({perc_all_gatcs_identified_in_bam} %)"
            ).format(**stats),
            "Number of GATCs NOT identified in the BAM file": (
                "{all_gatcs_not_identified_in_bam} "
                "({perc_all_gatcs_not_identified_in_bam} %)"
            ).format(**stats),
            "Number of GATCs in methylation report": (
                "{all_gatcs_in_meth} ({perc_all_gatcs_in_meth} %)"
            ).format(**stats),
            "Number of GATCs NOT in methylation report": (
                "{all_gatcs_not_in_meth} ({perc_all_gatcs_not_in_meth} %)"
            ).format(**stats),
        }

        # ...and about the methylations:
        methylations_dict = {
            "Total number of GATCs in all the analyzed molecules": (
                "{max_possible_methylations}".format(**stats)
                ),
            "Fully methylated": (
                "{fully_methylated_gatcs} "
                "({fully_methylated_gatcs_wrt_meth} %)"
                ).format(**stats),
            "Fully unmethylated": (
                "{fully_unmethylated_gatcs} "
                "({fully_unmethylated_gatcs_wrt_meth} %)"
                ).format(**stats),
            "Hemi-methylated...": (
                "{hemi_methylated_gatcs} ({hemi_methylated_gatcs_wrt_meth} %)"
                ).format(**stats),
            "...only in '+' strand": (
                "{hemi_plus_methylated_gatcs} "
                "({hemi_plus_methylated_gatcs_wrt_meth} %)"
                ).format(**stats),
            "...only in '-' strand": (
                "{hemi_minus_methylated_gatcs} "
                "({hemi_minus_methylated_gatcs_wrt_meth} %)"
                ).format(**stats),
        }

        custom_images = {
            k: v.format(prefix=self.partition_prefix)
            for k, v in SM_ANALYSIS_IMAGES.items()
        }
        self.expected_summary = {
            "title": "sm-analysis · summary report",
            overview_head: overview_dict,
            results_head: results_dict,
            bam_file_head: bam_dict,
            reference_file_head: reference_dict,
            mols_subs_head: molecules_subreads_dict,
            seq_coverage_head: seq_coverage_dict,
            GATCs_head: GATCs_dict,
            methylations_head: methylations_dict,
            "images": [
                {"src": "{molecule_type_bars}".format(**custom_images),
                     "alt": "count of molecule types"
                 },
                {"src": "{molecule_len_histogram}".format(
                    **custom_images),
                    "alt": "molecule length histogram"
                 },
                {"src": "{position_coverage_bars}".format(
                    **custom_images),
                    "alt": (
                        "Position coverage in BAM file and in Methylation "
                        "report")
                 },
                {"src": "{position_coverage_history}".format(
                    **custom_images),
                    "alt": "Sequencing position coverage history"
                 },
                {"src": "{gatc_coverage_bars}".format(**custom_images),
                    "alt": "GATC coverage"},
                {"src": "{meth_type_bars}".format(**custom_images),
                    "alt": "count of methylation types"},
            ]
        }

    def check_summary_report_created(self):
        with open(self.found_summary_report) as summary_report_f:
            report_text = summary_report_f.read()
        parser = SummaryReportParser()
        parser.feed(report_text)

        self.check_and_update_date_in_summary_report(parser.parsed_data)

        # For debugging the next splitting makes things easier:
        for key, value in self.expected_summary.items():
            got_value = parser.parsed_data[key]
            assert got_value == value, f"{key=}\n{value=}\n{got_value=}"
        # ...if the previous part is enabled, the next is redundant:
        assert parser.parsed_data == self.expected_summary

        # Finally he checks that the report includes some images:
        # (yes, this is quite smocky: only testing that a file exists and it
        # is an image by inspecting the header)
        assert len(parser.images) == len(self.expected_summary["images"])
        for image in parser.images:
            assert image in self.expected_summary["images"]
            image_path = Path(image["src"])
            assert image_path.is_file()
            ext = image_path.suffix.strip(".")
            assert ext == imghdr.what(image_path)

    def check_and_update_date_in_summary_report(self, current_data):
        key = (
            "Summary report: Single Molecule Methylation Analysis >> Overview"
        )
        expected_datetime_iso = self.expected_summary[key]["Date"]
        current_datetime_iso = current_data[key]["Date"]
        expected_datetime = datetime.fromisoformat(expected_datetime_iso)
        current_datetime = datetime.fromisoformat(current_datetime_iso)
        assert abs(expected_datetime-current_datetime) < timedelta(seconds=300)
        # Once we are sure that, within a safety margin, the dates agree,
        # the expected date is updated with the current, to simplify
        # comparisons later on...
        self.expected_summary[key]["Date"] = current_datetime_iso

    def check_unique_id_in_log_messages(self, raw_lines: list[str]) -> None:
        """Ensures that all log message contains a unique ID."""
        ids = set()
        for line in raw_lines:
            line = line.strip()
            if line.startswith("["):
                start_id = line.find("[", 1)+1
                end_id = line.find("]", start_id)
                ids.add(line[start_id:end_id])
        assert len(ids) <= 1
        if (unique_id := ids.pop()):
            assert set(unique_id) <= set("0123456789abcdef")

    def remove_marker_files(self):
        """Marker files are files generated by each process launched
        by fake tools as a cheap mean to signal that there was a process
        running. Since some FTs cound the number of marker files to
        determine if the behavior was correct, they must be cleaned up
        before running checks.
        This method removes the marker files generated by external tools.
        """
        cwd = Path(".")
        for tool in ("ccs", "ipdSummary", "blasr"):
            for markerfile in cwd.glob(f".{tool}.pid.*"):
                markerfile.unlink(missing_ok=True)

    def check_partition(self, options: Iterable[str], output: str):
        """Finds and validates the partition in ``options``."""
        for ioption, option in enumerate(options):
            if option in ("-P", "--partition"):
                raw_partition = options[ioption+1]
                break
        else:
            return
        err_msg = None
        try:
            partition, npartitions = [int(_) for _ in raw_partition.split(":")]
        except ValueError:
            err_msg = "Invalid syntax for the partition"
        else:
            if partition < 1 or partition > npartitions or npartitions < 1:
                err_msg = "The given partition is not valid"
        if err_msg:
            assert (
                f"{err_msg} ('{raw_partition}'). Using default partition."
            ) in output

    def check_sm_analysis_with_bam_and_expected_results(self, *options):
        """This function accepts an arbitrary number of options to recycle it
        for verbose/quiet runs.
        """
        self.remove_marker_files()
        options = self.clos+options
        bam = self.bam
        cmd = (bam, self.fasta)+options

        expected_blasr_calls = 4
        if self.blasr_ccs.exists():
            expected_blasr_calls -= 1
        if self.pi_shifted_blasr_ccs.exists():
            expected_blasr_calls -= 1

        need_to_do_blasr_ccs = not self.blasr_ccs.exists()

        if "-v" in options or "--verbose" in options:
            verbose = True
        else:
            verbose = False
        with run_sm_analysis(*cmd) as cmd_result:
            raw_output_lines = (
                cmd_result[0].stdout.decode().split("\n")
                + cmd_result[0].stderr.decode().split("\n")
            )
            self.check_unique_id_in_log_messages(raw_output_lines)
            clean_stdout = normalize_whitespaces(cmd_result[0].stdout.decode())
            clean_stderr = normalize_whitespaces(cmd_result[0].stderr.decode())
            output = clean_stdout+clean_stderr
            # and he finds no critical errors:
            actual_msg = f"Actual output:\n{output}"
            for error_indicator in ("critical",):
                assert error_indicator not in output.lower(), actual_msg
            assert len(clean_stdout) == 0
            # and the return code of the program is 0, which reassures him:
            cmd_result[0].check_returncode()
        self.make_expected_summary_report(options)
        # he inspects more carefully the output:
        self.check_partition(options, output)
        assert f"Starting 'sm-analysis' (version {VERSION}) with:" in output
        assert f"Input BAM file: '{bam}'" in output
        assert f"Reference file: '{self.fasta}'" in output

        self.check_ipdsummary_program_and_processes(
            options, output, cmd_result)

        if "--keep-temp-dir" in options:
            self.check_temp_files(
                output, self.one_mol_bams, self.rejected_molecules, options)

        self.check_modification_types(output, options)

        if self.unaligned_input:
            assert "The input BAM is NOT aligned" in output
            if self.aligned_bam:
                assert (
                    "...but a possible aligned version of the input BAM was "
                    f"found: 'blasr.{bam}'. It will be used.") in output
                expected_blasr_calls -= 1
            else:
                assert (
                    "...since no aligned version of the input BAM was found, "
                    f"one has been produced and it will be used: 'blasr.{bam}'"
                ) in output
            if self.pi_shifted_aligned_bam:
                assert (
                    "...but a possible pi-shifted aligned version of the input"
                    f" BAM was found: 'pi-shifted.blasr.{bam}'. It will be "
                    "used."
                ) in output
                expected_blasr_calls -= 1
            else:
                assert (
                    "...since no pi-shifted aligned version of the input BAM "
                    "was found, one has been produced and it will be used: "
                    f"'pi-shifted.blasr.{bam}'"
                ) in output
        else:
            expected_blasr_calls -= 2
            assert "The input BAM is aligned" in output
            if self.pi_shifted_aligned_bam:
                assert (
                    f"...a possible pi-shifted aligned version of the "
                    f"input BAM was found: '{self.pi_shifted_aligned_bam}'. It"
                    " will be used."
                ) in output
            else:
                assert (
                    "...but no pi-shifted aligned version of the input BAM "
                    "was found"
                ) in output
                assert (
                    "...therefore the pi-shifted analysis is disabled"
                ) in output
                expected_blasr_calls //= 2
        # Just to be sure that ugly warning messages from Pysam are not there:
        assert (
            "[E::idx_find_and_load] Could not retrieve index "
            "file for"
        ) not in output

        if "--only-produce-methylation-report" not in options:
            assert ("[filter] Sieving molecules from input BAM "
                    "before the IPD analysis") in output
            if verbose:
                for rejected_molecule in self.rejected_molecules:
                    assert (f"[filter] Molecule '{rejected_molecule}' rejected"
                            ) in output

        missing_aligned_ccs_msg = (
            "The methylation analysis requires aligned CCS files --for all "
            "variants-- to proceed. Trying to get them..."
        )
        missing_ccs_msg = MISSING_CCS_MSG
        ccs_generated_msg = f"[ccs] File 'ccs.{bam}' generated"
        aligned_ccs_generated_msg = (
            f"[blasr] Aligned file 'blasr.ccs.{bam}' generated"
        )

        generate_mol_mapping_msgs = [
            "Generating molecules mapping from aligned CCS file"
        ]
        # The first case is obvious; the second happens when the input is
        # aligned but there is a pi-shifted aligned file present:
        if self.unaligned_input or (self.pi_shifted_aligned_bam is not None):
            generate_mol_mapping_msgs.append(
                "Generating molecules mapping from pi-shifted aligned CCS file"
            )
        meth_report_produced_msg = (
            "[methylation report] Results saved to file "
            f"'{self.found_meth_report}'"
        )
        meth_msgs = [
            missing_aligned_ccs_msg,
            missing_ccs_msg,
            ccs_generated_msg,
        ] + generate_mol_mapping_msgs

        if need_to_do_blasr_ccs:
            meth_msgs.append(aligned_ccs_generated_msg)

        check_blasr = True
        check_ccs = True

        for arg in ("-C", "--CCS-bam-file"):
            if arg in options:
                ccs_bam_file = options[options.index(arg)+1]
                meth_msgs = [
                    missing_aligned_ccs_msg,
                    aligned_ccs_generated_msg
                ] + generate_mol_mapping_msgs
                check_ccs = False
                assert f"CCS bam file: '{ccs_bam_file}'" in output
                break

        if verbose:
            meth_msgs.append(
                f"ccs lines (aligned): {self.num_ccs_mols} molecules found"
            )
        for imperfect_mol in self.imperfect_molecules:
            meth_msgs.append(
                f"Molecule {imperfect_mol} discarded "
                f"due to DNA sequence mismatch with reference"
            )
        # (I add here the last methylation report-related message after all the
        # others):
        meth_msgs.append(meth_report_produced_msg)

        for msg in meth_msgs:
            assert msg in output, f"{msg=}\n{output=}\n"

        # The molecules having a perfect mapping should not be reported as
        # "discarded due to sequence mismatch":
        for mol in self.all_molecules:
            if mol not in self.imperfect_molecules:
                assert (
                    f"Molecule {mol} discarded "
                    "due to DNA sequence mismatch with reference"
                ) not in output

        aligner = "blasr"
        for arg in ("-b", "--blasr-path"):
            if arg in options:
                aligner = options[options.index(arg)+1]
                break
        assert f"aligner: '{aligner}'" in output

        nprocs_blasr = 1
        if "--nprocs-blasr" in options:
            nprocs_blasr = int(options[options.index("--nprocs-blasr")+1])
        assert f"# workers blasr: {nprocs_blasr}" in output
        if check_blasr:
            total_blasr_procs = expected_blasr_calls*nprocs_blasr
            assert total_blasr_procs == count_marker_files("blasr")
            # assert 2*nprocs_blasr == count_marker_files("blasr")
            # assert nprocs_blasr == cmd_result[1]["nprocs_blasr"]

        ccs_program = "ccs"
        for arg in ("-c", "--ccs-path"):
            if arg in options:
                ccs_program = options[options.index(arg)+1]
                break
        assert f"ccs program: '{ccs_program}'" in output

        if check_ccs:
            # Remember that this is artificial, only for the fake tool.
            # The real ccs uses more than one proc:
            assert 1 == count_marker_files("ccs")
            # assert 1 == cmd_result[1]["nprocs_ccs"]

        indexer = "pbindex"
        for arg in ("-p", "--pbindex-path"):
            if arg in options:
                indexer = options[options.index(arg)+1]
                break
        assert f"indexer: '{indexer}'" in output

        for faulty_mol, tool_info in self.faulty_molecules.items():
            tool = tool_info["tool"]
            tool_error = tool_info["error"]
            assert (
                f"[{tool}] Molecule {faulty_mol} could not be processed"
                in output
            )
            if verbose:
                assert f"[{tool}] The reported error was:" in output
                assert f"[{tool}]     '{tool_error}'" in output

        for arg in ("-M", "--ipd-model"):
            if arg in options:
                model = options[options.index(arg)+1]
                assert re.search(f"ipd model:.*{model}.*", output)
                break

        if "--only-produce-methylation-report" in options:
            assert "only produce methylation report: yes" in output

        assert re.search(
            r"Execution time [(]wall clock time[)]: \d+[.]\d* s = \d+[.]\d* h",
            output
        )

        self.check_one_molecule_bam_files_produced(output, options)

        # he sees that three new files have been created:
        # First, a joint gff file:
        if self.expected_gff:
            self.check_for_gff()
        # Also a summary per methylation found, in csv format:
        if self.expected_csv:
            self.check_for_csv(output)
        # and a summary of methylations per molecule is also produced,
        # in csv format too:
        assert self.found_meth_report.exists()
        with open(self.found_meth_report) as meth_report_f:
            with open(self.expected_meth_report) as expected_meth_report_f:
                assert expected_meth_report_f.read() == meth_report_f.read()
        # Last, but not least, a summary report in HTML format has been
        # created:
        self.check_summary_report_created()
