import argparse, json
from turtle import color
from termcolor import colored
from tabulate import tabulate
from os.path import exists
from model.common.wordmaker import WordMaker
import os

# Get project's home directory,
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# All data directory
DATADIR = os.path.abspath(os.path.join(BASEDIR, "data"))


def getArgs():
    parser = argparse.ArgumentParser(
        description="used for making excel based on model or checking excel data according to the model"
    )
    parser.add_argument("model", help="input program code: 0008 5669 5562 5406 ")
    parser.add_argument("-m", "--make", help="input excel file name for output")
    parser.add_argument(
        "-e",
        "--excel",
        help="input excel file name as data source for generating docx file",
    )
    parser.add_argument("-w", "--word", help="input word file name for output")
    parser.add_argument(
        "-r",
        "--rep_company",
        help="input rep's company short name for generating some customized docs",
    )
    parser.add_argument("-c", "--check", help="input excel file name to check")
    parser.add_argument("-j", "--json", help="output json data", action="store_true")

    args = parser.parse_args()
    args.rep_company = args.rep_company or "noah"
    return args


def getModels(args):
    models = {
        # Experience
        "exp-ec": {
            "path": "model.experience.ec",
            "class_list": ["EmploymentModel"],
            "remark": "Experience module for Employment Certificate model",
        },
        "exp-rs": {
            "path": "model.experience.resume",
            "class_list": ["ResumeModel"],
            "remark": "Experience module for Resume model",
        },
        # Recruitment
        "recruit-ja": {
            "path": "model.recruit.jobad",
            "class_list": ["JobadModel"],
            "remark": "Recruit module for Job Advertisement model",
        },
        "recruit-jo": {
            "path": "model.recruit.joboffer",
            "class_list": ["JobofferModel"],
            "remark": "Recruitment module for Job Offer model",
        },
        "recruit-rs": {
            "path": "model.recruit.recruitmentsummary",
            "class_list": ["RecruitmnetSummaryModel"],
            "remark": "Recruitment module for Recruitment Summary model",
        },
        # LMIA
        "lmia-ert": {
            "path": "model.lmia.employertraining",
            "class_list": ["EmployerTrainingModel"],
            "remark": "LMIA module for Employer Training model",
        },
        "lmia-sl": {
            "path": "model.lmia.submissionletter",
            "class_list": ["SubmissionLetterModel"],
            "remark": "LMIA module for Submission Letter model",
        },
        "lmia-st1": {
            "path": "model.lmia.stage1",
            "class_list": ["LmiaAssess"],
            "remark": "LMIA module for stage 1 model (assessment)",
        },
        "lmia-st2": {
            "path": "model.lmia.stage2",
            "class_list": ["LmiaRecruitment"],
            "remark": "LMIA module for stage 2 model (recruitment)",
        },
        "lmia-st3": {
            "path": "model.lmia.stage3",
            "class_list": ["LmiaApplication"],
            "remark": "LMIA module for for stage 3 model (application)",
        },
        # BCPNP
        "bcpnp-ert": {
            "path": "model.bcpnp.employertraining",
            "class_list": ["EmployerTrainingModel"],
            "remark": "BCPNP module for Employer Training model",
        },
        "bcpnp-eet": {
            "path": "model.bcpnp.employeetraining",
            "class_list": ["EmployeeTrainingModel"],
            "remark": "BCPNP module for Employee Training model",
        },
        "bcpnp-jd": {
            "path": "model.bcpnp.jobdescription",
            "class_list": ["JobDescriptionModel"],
            "remark": "BCPNP module for Job Description model",
        },
        "bcpnp-jof": {
            "path": "model.bcpnp.jobofferform",
            "class_list": ["JobOfferFormModel"],
            "remark": "BCPNP module for Job Offer Form model",
        },
        "bcpnp-rl": {
            "path": "model.bcpnp.recommendationletter",
            "class_list": ["RecommendationLetterModel"],
            "remark": "BCPNP module for Recommendation Letter model",
        },
        "bcpnp-rpf": {
            "path": "model.bcpnp.repform",
            "class_list": ["RepFormModel"],
            "remark": "BCPNP module for Representative Form model",
        },
        "bcpnp-reg": {
            "path": "webform.models.bcpnpmodel_reg",
            "class_list": ["BcpnpModelReg"],
            "remark": "BCPNP module for BCPNP Registration model",
        },
        "bcpnp-reg-ee": {
            "path": "webform.models.bcpnpmodel_reg",
            "class_list": ["BcpnpEEModelReg"],
            "remark": "BCPNP module for BCPNP Registration model(EE)",
        },
        "bcpnp-app": {
            "path": "webform.models.bcpnpmodel_app",
            "class_list": ["BcpnpModelApp"],
            "remark": "BCPNP module for BCPNP Application model",
        },
        "bcpnp-app-ee": {
            "path": "webform.models.bcpnpmodel_app",
            "class_list": ["BcpnpEEModelApp"],
            "remark": "BCPNP module for BCPNP application (EE) model",
        },
        # PR
        "0008": {
            "path": "model.pr.m0008",
            "class_list": ["M0008Model"],
            "remark": "PR module for form 0008 model",
        },
        "5406": {
            "path": "model.pr.m5406",
            "class_list": ["M5406Model"],
            "remark": "PR module for form 5406 model",
        },
        "5562": {
            "path": "model.pr.m5562",
            "class_list": ["M5562Model"],
            "remark": "PR module for form 5562 model",
        },
        "5669": {
            "path": "model.pr.m5669",
            "class_list": ["M5669Model"],
            "remark": "PR module for form 5669 model",
        },
        "pr": {
            "path": "webform.models.prmodel",
            "class_list": ["PrModel"],
            "remark": "PR module for all PR model",
        },
        # TR
        "0104": {
            "path": "model.tr.m0104",
            "class_list": ["M0104Model"],
            "remark": "TR module for form 0104 model",
        },
        "1294": {
            "path": "model.tr.m1294",
            "class_list": ["M1294Model"],
            "remark": "TR module for form 1294 model",
        },
        "1295": {
            "path": "model.tr.m1295",
            "class_list": ["M1295Model"],
            "remark": "TR module for form 1295 model",
        },
        "5257": {
            "path": "model.tr.m5257",
            "class_list": ["M5257Model"],
            "remark": "TR module for form 5257 model",
        },
        "5708": {
            "path": "model.tr.m5708",
            "class_list": ["M5708Model"],
            "docx_template": os.path.join(
                DATADIR, "word", f"{args.rep_company}-5708-sl.docx"
            ),
            "remark": "TR module for form 5708 model",
        },
        "5709": {
            "path": "model.tr.m5709",
            "class_list": ["M5709Model"],
            "remark": "TR module for form 5709 model",
        },
        "5710": {
            "path": "model.tr.m5710",
            "class_list": ["M5710Model"],
            "remark": "TR module for form 5710 model",
        },
    }

    return models


def makeExcel(args, the_model):
    file_exists = exists(args.make)
    if file_exists:
        overwrite = input(colored(f"{args.make} is existed, overwrite?(Y/N)"))
        if overwrite and overwrite.upper()[0] == "N":
            return
    # create excel
    the_model(output_excel_file=args.make)
    print(colored(f"{args.make} has been created", "green"))


def makeWord(args, model, the_model):
    word_file_exists = exists(args.word)
    excel_file_exists = exists(args.excel)
    if word_file_exists:
        overwrite = input(colored(f"{args.word} is existed, overwrite?(Y/N)"))
        if overwrite and overwrite.upper()[0] == "N":
            return
    if not excel_file_exists:
        print(colored(f"{args.excel} is not existed."))
        return

    template_docx = model.get("docx_template")
    if not template_docx:
        print(
            colored(
                f"There is no template existing in model {model.get('class_list')[0]}",
                "red",
            )
        )
        return
    if not exists(template_docx):
        print(
            colored(
                f"{template_docx} is not existed. Please check your template base",
                "red",
            )
        )
        return

    model = the_model(excels=[args.excel])
    wm = WordMaker(template_docx, model.getAllDict, args.word)
    wm.make()


def checkModel(args, the_model):
    model_obj = the_model(excels=[args.check])
    if model_obj.dict() != {}:
        print(
            json.dumps(model_obj.dict(), indent=3, default=str)
        ) if args.json else print(
            colored(f"The model is checked and everything seems good...", "green")
        )


def getHelp(valid_models):
    contents = [["Model", "Description", "Word Template"]]
    for model, value in valid_models.items():
        word_template = value.get("docx_template") or "Not available"
        contents.append([model, value["remark"], os.path.basename(word_template)])

    print(tabulate(contents, tablefmt="fancy_grid"))
    return


def main():
    args = getArgs()
    valid_models = getModels(args)  # some variables depending on args

    if not args.model:
        print(colored("You must input model!", "red"))
        exit(1)

    if args.model.upper() == "HELP":
        getHelp(valid_models)
        return

    if not valid_models.get(args.model):
        print(colored(f"Model ({args.model}) is not existed. Please check.", "red"))
        exit(1)

    # get model, and its instance
    model = valid_models.get(args.model)
    class_list = model["class_list"]
    the_class = __import__(model["path"], fromlist=class_list)
    the_model = getattr(the_class, class_list[0])

    # Make excel based on model
    if args.make:
        makeExcel(args, the_model)

    # Make document based on model and source excel data
    if args.excel and args.word:
        makeWord(args, model, the_model)

    # Check model, output error list or excel file, and generate json output if model is correct and required
    if args.check:
        checkModel(args, the_model)


if __name__ == "__main__":
    main()
