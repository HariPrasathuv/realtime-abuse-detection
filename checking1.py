
def load_detection_models():
    print("Detection MODELs Loading WAIT....")
    from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

    abuse_model = AutoModelForSequenceClassification.from_pretrained("./HateBert_abuseval/HateBert_abuseval")
    abuse_tokenizer = AutoTokenizer.from_pretrained("./HateBert_abuseval/HateBert_abuseval")
    abuseModel = pipeline("text-classification", model=abuse_model, tokenizer=abuse_tokenizer)

    hate_model = AutoModelForSequenceClassification.from_pretrained("./HateBert_hateval/HateBert_hateval")
    hate_tokenizer = AutoTokenizer.from_pretrained("./HateBert_hateval/HateBert_hateval")
    hateModel = pipeline("text-classification", model=hate_model, tokenizer=hate_tokenizer)

    offense_model = AutoModelForSequenceClassification.from_pretrained("./HateBert_offenseval/HateBert_offenseval")
    offense_tokenizer = AutoTokenizer.from_pretrained("./HateBert_offenseval/HateBert_offenseval")
    offenseModel = pipeline("text-classification", model=offense_model, tokenizer=offense_tokenizer)

    print("===============================Detection Model Loaded==========================\n")
    return abuseModel,hateModel,offenseModel

def detect(text,abuseModel,hateModel,offenseModel):
    abuseResult = abuseModel(text)
    print("Abuse: ",abuseResult)

    offenseResult = offenseModel(text)
    print("Offense: ",offenseResult)
    hateResult = hateModel(text)
    print("Hate: ",hateResult)
    detectList = []
    
    if abuseResult[0]['label'] == 'LABEL_1' or offenseResult[0]['label'] == 'LABEL_1' or hateResult[0]['label'] == 'LABEL_1':
        
        if abuseResult[0]['label'] == 'LABEL_1':
            detectList.append(["Abuse",abuseResult[0]['score']])
        if offenseResult[0]['label'] == 'LABEL_1':
            detectList.append(["Offense",offenseResult[0]['score']])
        if hateResult[0]['label'] == 'LABEL_1':
            detectList.append(["Hate",hateResult[0]['score']])
        return 1,detectList


    return 0,detectList
