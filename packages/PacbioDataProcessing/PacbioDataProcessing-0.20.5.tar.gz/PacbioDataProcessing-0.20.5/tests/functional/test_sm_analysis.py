#######################################################################
#
# Copyright (C) 2020-2022 David Palao
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

"""Functional Tests for `sm-analysis` utility."""

import os
from pathlib import Path
import shutil
import subprocess as sp

from pacbio_data_processing.constants import SM_ANALYSIS_EXE

from .utils import (
    run_sm_analysis, normalize_whitespaces, temporarily_rename_file,
    remove_later, run_later, count_marker_files
)
from .common import SmAnalysisMixIn, MISSING_CCS_MSG


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR/"data"
GFF3_URL = (
    "https://github.com/The-Sequence-Ontology/Specifications/blob/master"
    "/gff3.md"
)
INSTALL_PBCORE = (
    "pip install git+https://github.com/PacificBiosciences/pbcore.git"
)
INSTALL_PBCOMMAND = (
    "pip install git+https://github.com/PacificBiosciences/pbcommand.git"
)
INSTALL_KINETICSTOOLS = (
    "pip install git+https://github.com/PacificBiosciences/kineticsTools.git"
)
INSTALL_EXTERNAL_TOOLS = (
    "https://pacbio-data-processing.readthedocs.io/en/latest/usage/"
    "installation.html#other-dependencies"
)


def clean_run_results(*paths):
    """Remove the files given after removing the prefix 'expected.' from
    the name of the file (the directory is excluded). E.g.
    clean_run_results(Path('/tmp/expected.myoutput.text'))

    will try to remove a file called '/tmp/myoutput.text'

    This function is useful if within a test case several runs of the
    same program are done (maybe with slightly different flags).
    """
    for path in paths:
        if path is None:
            continue
        if path.name.startswith("expected."):
            new_name = path.name[9:]
            to_rm = path.with_name(new_name)
        else:
            to_rm = path
        try:
            os.unlink(to_rm)
        except OSError as e:
            print(f"path={path.name}")
            print(f"Cannot delete file '{to_rm}'")
            print("Exception:")
            print(e)
            print("-"*50)


class TestCaseSmAnalysis:
    expected_help_lines = [
        "Single Molecule Analysis",
        "-h, --help show this help message and exit",
        "-v, --verbose",
        "--version show program's version number and exit",
        "-M MODEL, --ipd-model MODEL",
        (
            "model to be used by ipdSummary to identify the type of "
            "modification. MODEL must be either the model name or the "
            "path to the ipd model. "
            "First, the program will make an attempt "
            "to interprete MODEL as a path to a file defining a model; "
            "if that fails, MODEL will be understood to be "
            "the name of a model that must be "
            "accessible in the resources directory of kineticsTools "
            "(e.g. '-M SP3-C3' would trigger a "
            "search for a file called 'SP3-C3.npz.gz' within the "
            "directory with models provided by kineticsTools). "
            "If this option is not given, the default model in "
            "ipdSummary is used."
        ),
        "-b PATH, --blasr-path PATH path to blasr program (default: 'blasr')",
        (
            "-p PATH, --pbindex-path PATH path to pbindex program (default: "
            "'pbindex')"
        ),
        (
            "-i PATH, --ipdsummary-path PATH path to ipdSummary program "
            "(default: 'ipdSummary')"
        ),
        (
            "-N NUM, --num-simultaneous-ipdsummarys NUM number of simultaneous"
            " instances of ipdSummary that will cooperate to process the "
            "molecules (default: 1)"
        ),
        (
            "-n NUM, --num-workers-per-ipdsummary NUM number of worker proce"
            "sses that each instance of ipdSummary will spawn (default: 1)"
        ),
        (
            "--nprocs-blasr NUM number of worker processes "
            "that each instance of blasr will spawn (default: 1)"
        ),
        (
            "-P PARTITION:NUMBER-OF-PARTITIONS, --partition PARTITION:NUMBER-"
            "OF-PARTITIONS "
            "this option instructs the program to only analyze a fraction "
            "(partition) of the molecules present in the input bam file. The "
            "file is divided in `NUMBER OF PARTITIONS` (almost) equal pieces "
            "but ONLY the PARTITION-th partition (fraction) is analyzed. For "
            "instance, `--partition 3:7` means that the bam file is divided in"
            " seven pieces but only the third piece is analyzed by the current"
            " instance of sm-analysis. By default, all the file is analyzed."
        ),
        (
            "-c PATH, --ccs-path PATH path to ccs program (default: 'ccs')"
        ),
        (
            "-C BAM-FILE, --CCS-bam-file BAM-FILE "
            "the CCS file in BAM format can be optionally provided; otherwise "
            "it is computed. It is necessary to create the reference mapping "
            "between *hole numbers* and the DNA sequence of the corresponding "
            "fragment, or *molecule*. After being aligned, the file will be "
            "also used to determine the position of each molecule in the "
            "report of methylation states. If the CCS BAM file is provided, "
            "and any of the necessary aligned versions of it is not found, "
            "the CCS file will be aligned to be able to get the positions. "
            "If this option is not used, a CCS BAM will be generated "
            "from the original BAM file using the 'ccs' program"
        ),
        (
            "--keep-temp-dir should we make a copy of the temporary files "
            "generated? (default: False)"
        ),
        (
            "-m MOD-TYPE [MOD-TYPE ...], --modification-types MOD-TYPE "
            "[MOD-TYPE ...] focus only in the requested modification types "
            "(default: ['m6A'])"
        ),
        (
            "--only-produce-methylation-report "
            "use this flag to only produce the methylation report from the "
            "per detection csv file"
        ),
    ]

    def test_message_and_return_code_with_no_argument(self):
        #  Nathan is a new PhD student in the Biology department. He is working
        # in the analysis of DNA sequences.
        #  He needs to analyze the data coming from the expensive sequencer,
        # but has no idea about how to do it. Someone tells him about a
        # software called "PacbioDataProcessing". The name is promising. He
        # installs it and wants to try it.
        #  Reading the docs he learns that the package comes with a program
        # called 'sm-analysis' that seems to do what he looks after.
        #  First off he wants to test the program. How does it work? Why not
        # just run it?
        with run_sm_analysis() as plain_res:
            # he does so and he sees some clarifying error message:
            expected = [_.format(exe=SM_ANALYSIS_EXE) for _ in (
                "usage: {exe} [-h]",
                "[-v] [--version]",
                "{exe}: error: the following arguments are required:",
            )]
            for e in expected:
                assert e in normalize_whitespaces(plain_res[0].stderr.decode())
            # and it returns an error code to the terminal:
            assert plain_res[0].returncode != 0

    def test_help_run(self):
        # Ok, ok, he got it; he needs to call it with -h:
        with run_sm_analysis("-h") as help_res:
            # and, he gets a very informative message about its usage. Great!
            help_res_normalized = normalize_whitespaces(
                help_res[0].stdout.decode())
            for line in self.expected_help_lines:
                assert line in help_res_normalized
            # BTW, the returned code is not an error anymore:
            help_res[0].check_returncode()

    def test_version_option(self):
        # Nathan is curious about the version of the program he's using.
        with run_sm_analysis("--version") as version_res:
            version = version_res[0].stdout.decode().split(".")
            for i in version:
                int(i)


class TestCaseHappyPathSmAnalysis(SmAnalysisMixIn):
    def test_straight_run_with_only_bam_and_fai_files(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Nathan finds the killing program provided by the package:
        #  sm-analysis
        # It does exactly what he needs: single molecule analysis of
        # methylation states.
        # He learned that it must be run providing a bam file and a fasta file
        # afterwards, so he does:
        self.collect_opts_for_tests(sm_test_data)
        aligned_bams_to_rm = (self.aligned_bam, self.pi_shifted_aligned_bam)
        ccs_bam = self.bam.with_name("ccs."+self.bam.name)
        if "aligned present" in sm_test_data["features"]:
            aligned_bams_to_rm = ()
        elif "unaligned input" in sm_test_data["features"]:
            aligned_bams_to_rm = (
                self.bam.with_name("blasr."+self.bam.name),
                self.bam.with_name("pi-shifted.blasr."+self.bam.name)
            )
            self.aligned_bam = None
            self.pi_shifted_aligned_bam = None

        if len(self.clos) == 0:  # want to run without options in this FT
            if sm_test_data["name"] == (
                    "unaligned input with one mol crossing ori"):
                # In this case, the fixture provides some files that
                # must be deleted in the straight case:
                clean_run_results(*aligned_bams_to_rm)
            self.check_sm_analysis_with_bam_and_expected_results()
            ccs_files_to_remove = ccs_bam.parent.glob("*"+ccs_bam.stem+"*")
            clean_run_results(
                *aligned_bams_to_rm, *ccs_files_to_remove,
                self.found_gff, self.found_csv, self.found_meth_report
            )
            self.check_sm_analysis_with_bam_and_expected_results("--verbose")

    def test_different_combinations_of_aligned_files_unexpectedly_present(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Nathan runs the 'sm-analysis' program in a directory where he
        # previously ran it, with some files remaining...
        self.collect_opts_for_tests(sm_test_data)
        if sm_test_data["name"] == "unaligned input with one mol crossing ori":
            aligned_bam = self.aligned_bam
            pi_shifted_aligned_bam = self.pi_shifted_aligned_bam

            # 1) ∃ aligned and ∃ pi-shifted
            self.check_sm_analysis_with_bam_and_expected_results()
            clean_run_results(
                self.found_gff, self.found_csv, self.found_meth_report,
                self.ccs, self.blasr_ccs
            )
            self.check_sm_analysis_with_bam_and_expected_results("--verbose")
            clean_run_results(
                self.found_gff, self.found_csv, self.found_meth_report,
                self.ccs, self.blasr_ccs
            )
            # 2) ∃ aligned and ∄ pi-shifted
            self.pi_shifted_aligned_bam = None
            with temporarily_rename_file(pi_shifted_aligned_bam):
                self.check_sm_analysis_with_bam_and_expected_results()
                clean_run_results(
                    pi_shifted_aligned_bam, self.ccs, self.blasr_ccs,
                    self.found_gff, self.found_csv, self.found_meth_report
                )
                self.check_sm_analysis_with_bam_and_expected_results(
                    "--verbose")
                clean_run_results(
                    self.found_gff, self.found_csv, self.found_meth_report,
                    self.ccs, self.blasr_ccs
                )
            self.pi_shifted_aligned_bam = pi_shifted_aligned_bam
            # 3) ∄ aligned and ∃ pi-shifted
            self.aligned_bam = None
            with temporarily_rename_file(aligned_bam):
                self.check_sm_analysis_with_bam_and_expected_results()
                clean_run_results(
                    aligned_bam,
                    self.found_gff, self.found_csv, self.found_meth_report,
                    self.ccs, self.blasr_ccs
                )
                self.check_sm_analysis_with_bam_and_expected_results(
                    "--verbose")
                clean_run_results(
                    self.found_gff, self.found_csv, self.found_meth_report
                )
            self.aligned_bam = aligned_bam
        elif sm_test_data["name"] == "no clos":
            pi_shifted_aligned_bam = self.pi_shifted_aligned_bam
            # 5) input aligned and ∄ pi-shifted
            clean_run_results(pi_shifted_aligned_bam)
            self.check_sm_analysis_with_bam_and_expected_results()
            clean_run_results(
                pi_shifted_aligned_bam, self.ccs, self.blasr_ccs,
                self.found_gff, self.found_csv, self.found_meth_report
            )
            self.check_sm_analysis_with_bam_and_expected_results("--verbose")

    def test_ipd_model(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # One thing that Nathan is interested to test has to do with some
        # exotic data he has that he wants to analyze with a special ipd
        # model. Therefore, he wants to run sm-analysis with -M. He tries
        # it out:
        self.collect_opts_for_tests(sm_test_data)
        if ("-M" in self.clos) or ("--ipd-model" in self.clos):
            self.check_sm_analysis_with_bam_and_expected_results()
            clean_run_results(
                self.found_gff, self.found_csv, self.found_meth_report,
                self.ccs, self.blasr_ccs
            )
            self.check_sm_analysis_with_bam_and_expected_results("--verbose")

    def _test_run_including_preprocessing_to_align_input(self):
        ...

    def test_without_aligner_program(
            self, sm_test_data_baseline, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr_no_path):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan does not have the aligner in the path. What happens if
        # he runs the analysis like this?
        try:
            self.check_sm_analysis_with_bam_and_expected_results()
        except AssertionError as e:
            assert "CRITICAL" in str(e)
            assert "No such file or directory: 'blasr'" in str(e)
            assert "To install it, follow the instructions in:" in str(e)
            assert f"{INSTALL_EXTERNAL_TOOLS}" in str(e)
        else:
            assert False, "The expected error did not occur!"

    def test_choose_aligner_program(
            self, sm_test_data_baseline, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr_no_path):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan wants to use an aligner that is not in the path.
        # He needs to use a command line option for that with the path to an
        # executable that he wants to use as aligner. He launches the analysis
        # with such an argument:
        self.check_sm_analysis_with_bam_and_expected_results(
            "-b", "bin.no.path/blasr"
        )

    def test_without_indexer_program(
            self, sm_test_data_baseline, install_ipdSummary, install_ccs,
            install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan does not have the indexer in the path. What happens if
        # he runs the analysis like this?
        try:
            self.check_sm_analysis_with_bam_and_expected_results()
        except AssertionError as e:
            assert "CRITICAL" in str(e)
            assert "No such file or directory: 'pbindex'" in str(e)
            assert "To install it, follow the instructions in:" in str(e)
            assert f"{INSTALL_EXTERNAL_TOOLS}" in str(e)
        else:
            assert False, "The expected error did not occur!"

    def test_choose_indexer_program(
            self, sm_test_data_baseline, install_pbindex_no_path,
            install_ipdSummary, install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan does not have the indexer in the path. What happens if
        # he runs the analysis like this?
        # He knows that he needs to provide the path to an executable that he
        # wants to use as indexer. He launches the analysis with such an
        # argument:
        self.check_sm_analysis_with_bam_and_expected_results(
            "-p", "bin.no.path/pbindex"
        )

    def test_without_ccs_program(
            self, sm_test_data_baseline, install_pbindex, install_ipdSummary,
            install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan does not have the ccs program in the path. What happens
        # if he runs the analysis like this?
        try:
            self.check_sm_analysis_with_bam_and_expected_results()
        except AssertionError as e:
            assert "CRITICAL" in str(e)
            assert "No such file or directory: 'ccs'" in str(e)
            assert "To install it, follow the instructions in:" in str(e)
            assert f"{INSTALL_EXTERNAL_TOOLS}" in str(e)
        else:
            assert False, "The expected error did not occur!"

    def test_choose_ccs_program(
            self, sm_test_data_baseline, install_pbindex, install_ipdSummary,
            install_ccs_no_path, install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan does not have the ccs program in the path. What happens
        # if he runs the analysis like this?
        # He learned that he can provide the path to an executable that
        # he wants to use as ccs program. He launches the analysis with
        # such an argument:
        self.check_sm_analysis_with_bam_and_expected_results(
            "-c", "bin.no.path/ccs"
        )

    def test_without_ipd_analysis_program(
            self, sm_test_data_baseline, install_pbindex,
            temporarily_unplug_ipdSummary, install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan does not have the ipd analysis program in the path.
        # What happens if he runs the analysis like this?
        try:
            self.check_sm_analysis_with_bam_and_expected_results()
        except AssertionError as e:
            assert "CRITICAL" in str(e)
            assert "No such file or directory: 'ipdSummary'" in str(e)
            assert "It can be installed with:" in str(e)
            assert f"{INSTALL_PBCORE}" in str(e)
            assert f"{INSTALL_PBCOMMAND}" in str(e)
            assert f"{INSTALL_KINETICSTOOLS}" in str(e)
        else:
            assert False, "Expected a failure and didn't happen."

    def test_choose_ipd_analysis_program(
            self, sm_test_data_baseline, install_pbindex,
            install_ipdSummary_no_path, install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Now, Nathan does provide the path to the ipd analysis program.
        # He launches the analysis with such an argument:
        self.check_sm_analysis_with_bam_and_expected_results(
            "-i", "bin.no.path/ipdSummary"
        )

    def test_run_several_instances_of_ipd_analysis_program(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Since the time needed to process large bam files is long, Nathan
        # wonders what happens if he uses the -N option:
        self.collect_opts_for_tests(sm_test_data)
        # hence, Nathan provides the number of simultaneous instances of the
        # ipd analysis program. He launches the analysis with such an argument:
        if sm_test_data["name"] == "no clos":
            self.check_sm_analysis_with_bam_and_expected_results("-N", "3")

    def test_run_with_num_workers_for_ipd_analysis(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Another interesting option to explore is -n: it seems to allow
        # to run ipdSummary with several workers. It is worth exploring:
        self.collect_opts_for_tests(sm_test_data)
        # hence, Nathan provides the number of simultaneous instances of the
        # ipd analysis program. He launches the analysis with such an argument:
        if sm_test_data["name"] == "no clos":
            self.check_sm_analysis_with_bam_and_expected_results("-n", "5")

    def test_run_with_num_workers_for_alignment(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Yet another interesting option to explore is --nprocs-blasr:
        # it seems to further speed up the process by launching the aligner
        # with more than 1 worker. He gives it a try:
        self.collect_opts_for_tests(sm_test_data)
        # hence, Nathan provides the number of simultaneous instances of the
        # ipd analysis program. He launches the analysis with such an argument:
        if sm_test_data["name"] == "no clos":
            self.check_sm_analysis_with_bam_and_expected_results(
                "--nprocs-blasr", "3"
            )

    def _test_restart_run(self):
        ...

    def test_choose_modification_types(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # What if he is interested in different type of modifications?
        # The -m option of sm-analysis seems to be the answer. He tries it:
        self.collect_opts_for_tests(sm_test_data)
        # hence, Nathan provides the number of simultaneous instances of the
        # ipd analysis program. He launches the analysis with such an argument:
        if sm_test_data["name"] == "two modification types":
            self.check_sm_analysis_with_bam_and_expected_results(
                "-m", "m6A", "m4C")

    def test_run_with_partition(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Nathan has troubles with the speed of the analysis. Since he has
        # to analze large files with many molecules, and since most of the
        # analysis for each molecule is independent of the other molecules,
        # he would like to divide the file in pieces each processed
        # independently.
        # The sm-analysis program has an option for that (-P/--partition);
        # hence he chooses a test BAM file to try it.
        self.collect_opts_for_tests(sm_test_data)
        # He goes to a newly created directory, copies the file there,
        # and he runs the program on it:
        if sm_test_data["name"] == "partition2of3":
            self.check_sm_analysis_with_bam_and_expected_results()
            clean_run_results(
                self.found_gff, self.found_csv, self.found_meth_report,
                self.ccs, self.blasr_ccs
            )
            self.check_sm_analysis_with_bam_and_expected_results("--verbose")

    def test_run_with_aligned_CCS_bam_file(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs):
        self.collect_opts_for_tests(sm_test_data)
        # Since the production of the CCS file takes some time, Nathan
        # would like to recycle its aligned version. Would it work if
        # he simply copies the file?
        if sm_test_data["name"] == "no clos":
            # he copies the aligned CCS file the he wants to use to
            # the current working dir:
            shutil.copy(DATA_DIR/self.blasr_ccs.name, ".")
            self.check_sm_analysis_with_bam_and_expected_results()
            clean_run_results(
                self.found_gff, self.found_csv, self.found_meth_report,
                self.ccs
            )
            self.check_sm_analysis_with_bam_and_expected_results("--verbose")

    def test_run_with_CCS_bam_file_without_aligned_one(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_blasr):
        self.collect_opts_for_tests(sm_test_data)
        # Since the production of the CCS file takes some time, Nathan wants to
        # recycle it. But he didn't run it through 'blasr', thankfully he finds
        # the option to provide a raw --not aligned-- ccs file: -C
        # Here he goes:
        if sm_test_data["name"] == "no clos":
            # he copies the aligned CCS file the he wants to use to
            # the current working dir:
            shutil.copy(DATA_DIR/self.ccs.name, ".")
            clos = ("-C", f"{self.ccs.name}")
            self.check_sm_analysis_with_bam_and_expected_results(*clos)
            clean_run_results(
                self.found_gff, self.found_csv, self.found_meth_report,
                self.blasr_ccs
            )
            self.check_sm_analysis_with_bam_and_expected_results(
                *clos, "--verbose")

    def test_keeping_the_temporary_directory(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_test_data)
        # One thing Nathan is wishing to do is inspecting the one-molecule
        # intermediate files produced in the analysis. He finds an option
        # for that: --keep-temp-dir
        if sm_test_data["name"] == "no clos":
            self.check_sm_analysis_with_bam_and_expected_results(
                "--keep-temp-dir"
            )
            clean_run_results(
                self.found_gff, self.found_csv, self.found_meth_report,
                self.ccs, self.blasr_ccs
            )
            self.check_sm_analysis_with_bam_and_expected_results(
                "--keep-temp-dir", "--verbose"
            )

    def test_can_produce_just_methylation_reports(
            self, sm_test_data, install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_test_data)
        # Nathan has satisfactorily run sm-analysis to produce some data
        # and wants to re-produce the methylation report. Thankfully there
        # is an option for that. He runs the code with that option to see if
        # it works well:
        if sm_test_data["name"] == "no clos":
            gff = sm_test_data["gff"]
            shutil.copy2(gff, gff.with_name(gff.name[9:]))
            csv = sm_test_data["csv"]
            shutil.copy2(csv, csv.with_name(csv.name[9:]))
            self.expected_gff = None
            self.expected_csv = None
            self.check_sm_analysis_with_bam_and_expected_results(
                "--only-produce-methylation-report"
            )
            clean_run_results(self.found_meth_report, self.ccs, self.blasr_ccs)
            self.check_sm_analysis_with_bam_and_expected_results(
                "--only-produce-methylation-report", "--verbose"
            )


class TestCaseErrors(SmAnalysisMixIn):
    def test_wrong_type_of_files_passed_as_input(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Nathan passes by accident the wrong files to sm-analysis:
        bam = sm_test_data["bam"]
        fasta = sm_test_data["fasta"]
        cmd = (fasta, bam)
        with run_sm_analysis(*cmd) as cmd_result:
            clean_stdout = normalize_whitespaces(cmd_result[0].stdout.decode())
            clean_stderr = normalize_whitespaces(cmd_result[0].stderr.decode())
            output = clean_stdout+clean_stderr
            # and he finds a critical error:
            assert "critical" in output.lower(), f"Actual output:\n{output}"
            assert len(clean_stdout) == 0
            # and the return code of the program is not 0, which is a clear
            # sign that there was a problem:
            assert cmd_result[0].returncode != 0

    def test_wrong_model_name_passed_as_input(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        # Nathan makes a typo passing the name of the model:
        clos = sm_test_data["CLOs"]
        for arg in ("-M", "--ipd-model"):
            if arg in clos:
                model_idx = clos.index(arg)+1
                clos = list(clos)
                fake_model_path = "/tmp/icannotexist_nunca"
                while Path(fake_model_path).is_file():
                    fake_model_path += "."
                clos[model_idx] = fake_model_path
                bam = sm_test_data["bam"]
                fasta = sm_test_data["fasta"]
                cmd = (bam, fasta)+tuple(clos)
                with run_sm_analysis(*cmd) as cmd_result:
                    # clean_stdout = normalize_whitespaces(
                    #     cmd_result[0].stdout.decode())
                    clean_stderr = normalize_whitespaces(
                        cmd_result[0].stderr.decode())
                    assert (f"Model '{fake_model_path}' not found. "
                            "Using default model") in clean_stderr
                break

    def check_error_msgs_in_ccs(
            self, bam, fasta, *,
            check_critical=False,
            check_could_not=False,
            check_stderr=False,
            check_suspucious=False,
            check_stderr_empty=False
    ):
        ccs_bam_file = bam.with_name("ccs."+bam.name)
        cmd = (bam, fasta)
        with run_sm_analysis(*cmd) as cmd_result:
            clean_stdout = normalize_whitespaces(
                cmd_result[0].stdout.decode())
            clean_stderr = normalize_whitespaces(
                cmd_result[0].stderr.decode())
            output = clean_stdout+clean_stderr
        # and he finds a critical error:
        if check_critical:
            assert "critical" in output.lower(), f"Actual output:\n{output}"
        if check_could_not:
            assert (
                f"[CRITICAL] CCS BAM file '{ccs_bam_file}' could not "
                "be produced."
            ) in output
        if check_suspucious:
            assert (
                f"Although the file '{ccs_bam_file}' has been generated,"
                " there was an error.") in output
            assert (
                "It is advisable to check the correctness of the "
                "generated ccs file."
            ) in output
            assert (
                "[ccs] The following command was issued:"
            ) in output
            assert f"'ccs {bam} {ccs_bam_file}'" in output
        if check_stderr:
            assert (
                "[ccs] ...the error message was: 'libchufa.so not found'"
            ) in output
        elif check_stderr_empty:
            assert (
                "[ccs] ...but the program did not report any error message."
            ) in output
        if check_could_not:
            # and the return code of the program is not 0, which is a clear
            # sign that there was a problem:
            assert cmd_result[0].returncode != 0
            # and indeed the file was not produced
            assert not ccs_bam_file.exists()
        else:
            # and the return code of the program is 0:
            assert cmd_result[0].returncode == 0
            # and indeed the file was produced
            assert ccs_bam_file.exists()

    def test_ccs_does_not_produce_its_output_and_gives_error(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs_without_result_with_error, install_blasr):
        # Nathan ran 'sm-analysis' but the ccs program did not
        # create a ccs file. He's pleased to see that the
        # program displays an informative message and stops:
        if sm_test_data["name"] == "no clos":
            bam = sm_test_data["bam"]
            fasta = sm_test_data["fasta"]
            self.check_error_msgs_in_ccs(
                bam, fasta,
                check_critical=True,
                check_could_not=True
            )

    def test_ccs_does_produce_its_output_but_gives_error(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs_with_error, install_blasr):
        # Nathan ran 'sm-analysis' with a new ccs program. This time a
        # ccs file has been created, but the process returned an error.
        # Once more, he's pleased to see that the
        # program displays an informative message:
        if sm_test_data["name"] == "no clos":
            bam = sm_test_data["bam"]
            fasta = sm_test_data["fasta"]
            self.check_error_msgs_in_ccs(
                bam, fasta,
                check_suspucious=True,
                check_stderr=True
            )

    def test_ccs_does_produce_its_output_but_gives_empty_error(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs_with_empty_error, install_blasr):
        # Nathan ran 'sm-analysis' with a new ccs program. This time a
        # ccs file has been created, but the process returned an error.
        # Once more, he's pleased to see that the
        # program displays an informative message:
        if sm_test_data["name"] == "no clos":
            bam = sm_test_data["bam"]
            fasta = sm_test_data["fasta"]
            self.check_error_msgs_in_ccs(
                bam, fasta,
                check_suspucious=True,
                check_stderr_empty=True
            )

    def test_ccs_does_not_produce_its_output_but_gives_no_error(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs_without_result, install_blasr):
        # Nathan ran 'sm-analysis' yet with another faulty ccs program.
        # This time it did not create a ccs file, although there was no
        # error. He's pleased to see that the program displays an
        # informative message and stops:
        if sm_test_data["name"] == "no clos":
            bam = sm_test_data["bam"]
            fasta = sm_test_data["fasta"]
            self.check_error_msgs_in_ccs(
                bam, fasta,
                check_critical=True,
                check_could_not=True,
            )

    def test_pbindex_fails(
            self, sm_faulty_mol_test_data, install_pbindex_1mol_fails,
            install_ipdSummary, install_ccs, install_blasr):
        # Nathan tries the tool again, but for some reason he
        # sees that a molecule is missing in the results, and
        # inspecting the logs, he realizes that pbindex could not
        # produce the required file:
        self.collect_opts_for_tests(sm_faulty_mol_test_data)
        for tool_info in self.faulty_molecules.values():
            tool_info["tool"] = "pbindex"
            tool_info["error"] = "who knows what happens here"
        self.check_sm_analysis_with_bam_and_expected_results()
        self.bam.with_name(
            "blasr."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "pi-shifted.blasr."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "ccs."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "blasr.ccs."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "pi-shifted.blasr.ccs."+self.bam.name).unlink(missing_ok=True)
        clean_run_results(
            self.found_gff, self.found_csv, self.found_meth_report,
        )
        self.check_sm_analysis_with_bam_and_expected_results("--verbose")

    def test_ipdSummary_fails(
            self, sm_faulty_mol_test_data, install_pbindex,
            install_ipdSummary_1mol_fails, install_ccs, install_blasr):
        # Nathan tries the tool again, but for some reason he
        # sees that a molecule is missing in the results, and
        # inspecting the logs, he realizes that ipdSummary could not
        # produce the required file:
        self.collect_opts_for_tests(sm_faulty_mol_test_data)
        for tool_info in self.faulty_molecules.values():
            tool_info["tool"] = "ipdSummary"
            tool_info["error"] = "whatever I feel like I wanna do"
        self.check_sm_analysis_with_bam_and_expected_results()
        self.bam.with_name(
            "blasr."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "pi-shifted.blasr."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "ccs."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "blasr.ccs."+self.bam.name).unlink(missing_ok=True)
        self.bam.with_name(
            "pi-shifted.blasr.ccs."+self.bam.name).unlink(missing_ok=True)
        clean_run_results(
            self.found_gff, self.found_csv, self.found_meth_report,
        )
        self.check_sm_analysis_with_bam_and_expected_results("--verbose")

    def test_wrong_partition(
            self, sm_test_data_baseline, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # Accidentally Nathan types a wrong partition. What will it happen?
        # He observes that an error message is displayed:
        self.check_sm_analysis_with_bam_and_expected_results("-P", "23")
        clean_run_results(
            self.blasr_bam, self.pi_shifted_blasr_bam, self.ccs,
            self.found_gff, self.found_csv, self.found_meth_report
        )
        # But, wait... What happens if he enters this?
        self.check_sm_analysis_with_bam_and_expected_results("-P", "23:1")
        clean_run_results(
            self.blasr_bam, self.pi_shifted_blasr_bam, self.ccs,
            self.found_gff, self.found_csv, self.found_meth_report
        )
        # And this?
        self.check_sm_analysis_with_bam_and_expected_results("-P", "a:4")
        # That is great: the program has a layer of validation that reassures
        # him.


class TestCaseProvidedCCS(SmAnalysisMixIn):
    def test_ccs_file_passed_in_cl_and_present(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        if sm_test_data["name"] == "unaligned input":
            self.collect_opts_for_tests(sm_test_data)
            # Nathan wants to inject the ccs file in the process,
            # so he calls directly the ccs tool:
            bam = self.bam
            ccs_name = "ccs."+bam.name
            ccs_path = bam.with_name(ccs_name)
            sp.run(["ccs", bam, ccs_path], stdout=sp.PIPE, stderr=sp.PIPE)
            self.remove_marker_files()
            # Nathan calls the sm-analysis program providing the path
            # to that file:
            cmd = (bam, self.fasta, "-C", ccs_path)
            with run_sm_analysis(*cmd) as cmd_result:
                clean_stdout = normalize_whitespaces(
                    cmd_result[0].stdout.decode())
                clean_stderr = normalize_whitespaces(
                    cmd_result[0].stderr.decode())
                output = clean_stdout+clean_stderr
            # he checks that the program did not compute the ccs file
            assert MISSING_CCS_MSG not in output
            # assert 0 == cmd_result[1]["nprocs_ccs"]
            assert 0 == count_marker_files("ccs")

    def test_ccs_computed_only_once(
            self, sm_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        if sm_test_data["name"] == "unaligned input":
            self.collect_opts_for_tests(sm_test_data)
            # Nathan wants to inject the ccs file in the process,
            # so he calls directly the ccs tool:
            bam = self.bam
            # Nathan calls the sm-analysis program
            cmd = (bam, self.fasta)
            with run_sm_analysis(*cmd) as cmd_result:
                clean_stdout = normalize_whitespaces(
                    cmd_result[0].stdout.decode())
                clean_stderr = normalize_whitespaces(
                    cmd_result[0].stderr.decode())
                output = clean_stdout+clean_stderr
            # he checks that the program did compute the ccs file only ONCE:
            assert MISSING_CCS_MSG in output
            new_output = output.replace(MISSING_CCS_MSG, "XXX", 1)
            assert MISSING_CCS_MSG not in new_output
            # assert 1 == cmd_result[1]["nprocs_ccs"]
            assert 1 == count_marker_files("ccs")


class TestCaseBlasrWIP(SmAnalysisMixIn):
    def make_alignment_bam_and_wip_names(self, bam=None, variant=""):
        if bam is None:
            bam = self.bam
        prefix = "blasr."
        if variant != "":
            prefix = variant+"."+prefix
        blasr_bam = bam.with_name(prefix+bam.name)
        blasr_wip = blasr_bam.with_name("."+blasr_bam.name+".wip")
        return blasr_bam, blasr_wip

    def check_blasr_msgs(
            self,
            blasr_calls: list[tuple] = None,
            blasr_found: list[tuple] = None,
            blasr_not_found: list[tuple] = None
    ) -> tuple[sp.CompletedProcess, str]:
        """Items in ``blasr_calls`` are:
        (blasr_bam: Path, fasta: Path, blasr_wip: Path)

        Items in ``blasr_found`` and in  ``blasr_not_found`` are:
        (blasr_bam: Path, variant: str)

        where variant is expected to be one of these:

        * ``aligned``
        * ``pi-shifted aligned``
        """
        cmd = (self.bam, self.fasta)
        if blasr_calls is None:
            blasr_calls = []
        if blasr_found is None:
            blasr_found = []
        if blasr_not_found is None:
            blasr_not_found = []
        for (blasr_bam, fasta, blasr_wip) in blasr_calls:
            blasr_cmd = ["blasr", self.bam, fasta, "--bam", "--out", blasr_bam]
            self.executor.submit(lambda: remove_later(3, blasr_wip))
            self.executor.submit(lambda: run_later(2.8, blasr_cmd))
            # blasr_wip.unlink()
        with run_sm_analysis(*cmd) as cmd_result:
            clean_stdout = normalize_whitespaces(
                cmd_result[0].stdout.decode())
            clean_stderr = normalize_whitespaces(
                cmd_result[0].stderr.decode())
            output = clean_stdout+clean_stderr
        # He checks that sm-analysis did not computed the aligned bam files:
        assert "The input BAM is NOT aligned" in output
        for (blasr_bam, variant) in blasr_found:
            if "ccs" in str(blasr_bam):
                inbam = "ccs"
            else:
                inbam = "input"
            assert (
                f"...but a possible {variant} version of the {inbam} BAM was "
                f"found: '{blasr_bam}'. It will be used."
            ) in output
            assert (
                f"...since no {variant} version of the {inbam} BAM was found, "
                f"one has been produced and it will be used: '{blasr_bam}'"
            ) not in output
        for (blasr_bam, variant) in blasr_not_found:
            if "ccs" in str(blasr_bam):
                inbam = "ccs"
            else:
                inbam = "input"
            assert (
                f"...but a possible {variant} version of the {inbam} BAM"
                f" was found: '{blasr_bam}'. It will be used."
            ) not in output
            assert (
                f"...since no {variant} version of the {inbam} BAM "
                "was found, one has been produced and it will be used: "
                f"'{blasr_bam}'"
            ) in output
        return cmd_result, output

    def test_both_wip_files_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        blasr_bam, blasr_wip = self.make_alignment_bam_and_wip_names()
        blasr_wip.touch()
        pi_shifted_blasr_bam, pi_shifted_blasr_wip = (
            self.make_alignment_bam_and_wip_names(variant="pi-shifted")
        )
        pi_shifted_blasr_wip.touch()
        # There is another simultaneous run of sm-analysis, but Nathan
        # tries to launch the program in parallel
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[
                (blasr_bam, self.fasta, blasr_wip),
                (pi_shifted_blasr_bam, self.pi_shifted_fasta,
                    pi_shifted_blasr_wip),
            ],
            blasr_found=[
                (blasr_bam, "aligned"),
                (pi_shifted_blasr_bam, "pi-shifted aligned"),
            ]
        )
        # assert 0 == cmd_result[1]["nprocs_blasr"]

    def test_one_wip_file_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        # He runs again sm-analysis while another instance is processing
        # the same file:
        blasr_bam, blasr_wip = self.make_alignment_bam_and_wip_names()
        blasr_wip.touch()
        pi_shifted_blasr_bam, pi_shifted_blasr_wip = (
            self.make_alignment_bam_and_wip_names(variant="pi-shifted")
        )
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(blasr_bam, self.fasta, blasr_wip)],
            blasr_found=[(blasr_bam, "aligned")],
            blasr_not_found=[(pi_shifted_blasr_bam, "pi-shifted aligned")]
        )
        # assert 1 == count_marker_files("blasr")

        blasr_bam.unlink()
        blasr_wip.touch()
        # He tries again, but now the file without wip is there:
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(blasr_bam, self.fasta, blasr_wip)],
            blasr_found=[
                (pi_shifted_blasr_bam, "pi-shifted aligned"),
                (blasr_bam, "aligned"),
            ]
        )
        # assert 1 == count_marker_files("blasr")

        # And the same happens the other way around: blasr <-> pi-shifted.blasr
        blasr_bam.unlink()
        pi_shifted_blasr_bam.unlink()
        pi_shifted_blasr_wip.touch()
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(pi_shifted_blasr_bam, self.pi_shifted_fasta,
                          pi_shifted_blasr_wip)],
            blasr_found=[(pi_shifted_blasr_bam, "pi-shifted aligned")],
            blasr_not_found=[(blasr_bam, "aligned")],
        )
        # assert 1 == count_marker_files("blasr")

        pi_shifted_blasr_bam.unlink()
        pi_shifted_blasr_wip.touch()
        # He tries again, but now the file without wip is there:
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(pi_shifted_blasr_bam, self.pi_shifted_fasta,
                          pi_shifted_blasr_wip)
                         ],
            blasr_found=[
                (blasr_bam, "aligned"),
                (pi_shifted_blasr_bam, "pi-shifted aligned")
            ]
        )
        # assert 1 == count_marker_files("blasr")

    def test_abandoned_wips_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        blasr_bam, blasr_wip = self.make_alignment_bam_and_wip_names()
        pi_shifted_blasr_bam, pi_shifted_blasr_wip = (
            self.make_alignment_bam_and_wip_names(variant="pi-shifted")
        )
        blasr_wip.touch()
        pi_shifted_blasr_wip.touch()
        # the files have been created long ago...
        t = blasr_wip.stat().st_mtime-1000
        os.utime(blasr_wip, times=(t, t))
        os.utime(pi_shifted_blasr_wip, times=(t, t))
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[
                (blasr_bam, self.fasta, blasr_wip),
                (pi_shifted_blasr_bam, self.pi_shifted_fasta,
                 pi_shifted_blasr_wip)
            ],
            blasr_not_found=[
                (blasr_bam, "aligned"),
                (pi_shifted_blasr_bam, "pi-shifted aligned")
            ]
        )
        assert (
            f"Abandoned sentinel '{blasr_wip}' detected; overwritten."
            in output
        )
        assert (
            f"Abandoned sentinel '{pi_shifted_blasr_wip}'"
            " detected; overwritten.") in output

    def test_both_ccs_wip_files_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        self.make_ccs()
        blasr_ccs_bam, blasr_ccs_wip = self.make_alignment_bam_and_wip_names(
            bam=self.ccs)
        blasr_ccs_wip.touch()
        pi_shifted_blasr_ccs_bam, pi_shifted_blasr_ccs_wip = (
            self.make_alignment_bam_and_wip_names(
                bam=self.ccs, variant="pi-shifted")
        )
        pi_shifted_blasr_ccs_wip.touch()
        # There is another simultaneous run of sm-analysis, but Nathan
        # tries to launch the program in parallel
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[
                (blasr_ccs_bam, self.fasta, blasr_ccs_wip),
                (pi_shifted_blasr_ccs_bam, self.pi_shifted_fasta,
                    pi_shifted_blasr_ccs_wip),
            ],
            blasr_found=[
                (blasr_ccs_bam, "aligned"),
                (pi_shifted_blasr_ccs_bam, "pi-shifted aligned"),
            ]
        )
        # assert 0 == cmd_result[1]["nprocs_blasr"]

    def test_two_blasrs_if_no_ccs_wip_files(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        self.make_ccs()
        # If Nathan runs sm-analysis without another instance already
        # running, 2 blasr instances run:
        cmd = (self.bam, self.fasta)
        with run_sm_analysis(*cmd):
            ...
        assert 4 == count_marker_files("blasr")

    def test_one_ccs_wip_file_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        self.make_ccs(missing_ok=True)
        # He runs again sm-analysis while another instance is processing
        # the same file:
        blasr_ccs_bam, blasr_ccs_wip = self.make_alignment_bam_and_wip_names(
            bam=self.ccs)
        blasr_ccs_wip.touch()
        pi_shifted_blasr_ccs_bam, pi_shifted_blasr_ccs_wip = (
            self.make_alignment_bam_and_wip_names(
                bam=self.ccs, variant="pi-shifted"
            )
        )
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(blasr_ccs_bam, self.fasta, blasr_ccs_wip)],
            blasr_found=[(blasr_ccs_bam, "aligned")],
            blasr_not_found=[(pi_shifted_blasr_ccs_bam, "pi-shifted aligned")]
        )
        # assert 1 == count_marker_files("blasr")

        blasr_ccs_bam.unlink()
        blasr_ccs_wip.touch()
        # He tries again, but now the file without wip is there:
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(blasr_ccs_bam, self.fasta, blasr_ccs_wip)],
            blasr_found=[
                (pi_shifted_blasr_ccs_bam, "pi-shifted aligned"),
                (blasr_ccs_bam, "aligned")
            ]
        )
        # assert 1 == count_marker_files("blasr")

        # And the same happens the other way around: blasr <-> pi-shifted.blasr
        blasr_ccs_bam.unlink()
        pi_shifted_blasr_ccs_bam.unlink()
        pi_shifted_blasr_ccs_wip.touch()
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(pi_shifted_blasr_ccs_bam, self.pi_shifted_fasta,
                          pi_shifted_blasr_ccs_wip)],
            blasr_found=[(pi_shifted_blasr_ccs_bam, "pi-shifted aligned")],
            blasr_not_found=[(blasr_ccs_bam, "aligned")],
        )
        # assert 1 == count_marker_files("blasr")

        pi_shifted_blasr_ccs_bam.unlink()
        pi_shifted_blasr_ccs_wip.touch()
        # He tries again, but now the file without wip is there:
        cmd_result, output = self.check_blasr_msgs(
            blasr_calls=[(pi_shifted_blasr_ccs_bam, self.pi_shifted_fasta,
                          pi_shifted_blasr_ccs_wip)
                         ],
            blasr_found=[
                (blasr_ccs_bam, "aligned"),
                (pi_shifted_blasr_ccs_bam, "pi-shifted aligned")
            ]
        )
        # assert 1 == count_marker_files("blasr")

    def test_abandoned_ccs_wips_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        self.make_ccs(missing_ok=True)
        blasr_ccs_bam, blasr_ccs_wip = self.make_alignment_bam_and_wip_names(
            bam=self.ccs)
        pi_shifted_blasr_ccs_bam, pi_shifted_blasr_ccs_wip = (
            self.make_alignment_bam_and_wip_names(
                bam=self.ccs, variant="pi-shifted"
            )
        )
        blasr_ccs_wip.touch()
        pi_shifted_blasr_ccs_wip.touch()
        # the files have been created long ago...
        t = blasr_ccs_wip.stat().st_mtime-1000
        os.utime(blasr_ccs_wip, times=(t, t))
        os.utime(pi_shifted_blasr_ccs_wip, times=(t, t))
        cmd_result, output = self.check_blasr_msgs(
            blasr_not_found=[
                (blasr_ccs_bam, "aligned"),
                (pi_shifted_blasr_ccs_bam, "pi-shifted aligned")
            ]
        )
        assert (f"Abandoned sentinel '{blasr_ccs_wip}' detected; "
                "overwritten.") in output
        assert (f"Abandoned sentinel '{pi_shifted_blasr_ccs_wip}' detected; "
                "overwritten.") in output


class TestCaseCCSWIP(SmAnalysisMixIn):
    def make_ccs_bam_and_wip_names(self):
        ccs_bam = self.bam.with_name("ccs."+self.bam.name)
        ccs_wip = ccs_bam.with_name("."+ccs_bam.name+".wip")
        return ccs_bam, ccs_wip

    def test_wip_file_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        ccs_bam, ccs_wip = self.make_ccs_bam_and_wip_names()
        ccs_wip.touch()
        # There is another simultaneous run of sm-analysis, but Nathan
        # tries to launch the program in parallel
        self.executor.submit(lambda: remove_later(3, ccs_wip))
        self.executor.submit(lambda: run_later(2.8, self.make_ccs))
        cmd = (self.bam, self.fasta, "--verbose")
        with run_sm_analysis(*cmd) as cmd_result:
            clean_stdout = normalize_whitespaces(
                cmd_result[0].stdout.decode())
            clean_stderr = normalize_whitespaces(
                cmd_result[0].stderr.decode())
            output = clean_stdout+clean_stderr
        # He checks that sm-analysis did not compute the ccs bam file:
        assert (
            f"CCS file '{ccs_bam}' found. Skipping its computation."
        ) in output
        assert 0 == count_marker_files("ccs")

    def test_abandoned_wip_present(
            self, sm_wip_test_data, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_wip_test_data)
        ccs_bam, ccs_wip = self.make_ccs_bam_and_wip_names()
        ccs_wip.touch()
        # the file has been created long ago...
        t = ccs_wip.stat().st_mtime-1000
        os.utime(ccs_wip, times=(t, t))
        cmd = (self.bam, self.fasta)
        with run_sm_analysis(*cmd) as cmd_result:
            clean_stdout = normalize_whitespaces(
                cmd_result[0].stdout.decode())
            clean_stderr = normalize_whitespaces(
                cmd_result[0].stderr.decode())
            output = clean_stdout+clean_stderr
        # This time the program informs him about an old sentinel file.
        assert (
            f"CCS file '{ccs_bam}' found. Skipping its computation."
        ) not in output
        assert (
            f"Abandoned sentinel '{ccs_wip}' detected; overwritten."
        ) in output
        assert (
            "Aligned CCS file cannot be produced without CCS file. "
            "Trying to produce it..."
        ) in output
        # And he checks that sm-analysis did compute the ccs bam file:
        assert 1 == count_marker_files("ccs")


class TestCaseNoFastaIndex(SmAnalysisMixIn):
    def test_run_without_fasta_fai_file(
            self, sm_test_data_baseline, install_pbindex, install_ipdSummary,
            install_ccs, install_blasr):
        self.collect_opts_for_tests(sm_test_data_baseline)
        # By accident, Nathan removes the fasta.fai file:
        sm_test_data_baseline["fasta.fai"].unlink()
        # but he still tries to run sm-analysis. Hopefully it works...
        self.check_sm_analysis_with_bam_and_expected_results()
        # And indeed it does!
