# From copilot

import re, sys, pdfplumber


# Extract data for this calculator:
#  https://www.longevity-tools.com/levine-pheno-age#?S-albumin=4.6&S-creatinine=80&S-glucose=92&S-hsCRP=0.55&LYM=32.5&MCV=86&RDW=13.8&S-ALP=45&WBC=4.5&age=42

import pdfplumber

def parse_labcorp_report(pdf_path, measurements_to_extract):
    measurements = {key: None for key in measurements_to_extract}
#   print("Measurements to extract: " , measurements)

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            for line in lines:
#               print("db0:" + line)
                for measurement in measurements_to_extract:
                    measurement2 = "^" + re.escape(measurement) + " " # escape () etc
#                   print("db1:" + measurement2 + ' ' + line)
                    if re.search(measurement2, line):
#                       parts = line.split()
                        pattern = r'\b\d+\.?\d*+\b'
                        parts = re.findall(pattern, line)
#                       print("db2:" + measurement, parts)
                        if (len(parts) > 1):
                            value = parts[0]
                            if (value == '01' or value == '02'):
                                value = parts[1]
#                           print("db3:" + measurement + '=' + value)
                            measurements[measurement] = value
                            break

    return measurements

def extract_value(line):
    # This function extracts the numerical value from a line of text
    parts = line.split()
    print(parts)
    if (len(parts) < 4):
        print("Error parsing: " , parts)
        return None
    value = parts[1]
    if (value == '01' or value == '02'):
        value = parts[2]
    return value
        
#    for part in parts:
#        print("part=" + part)
#       try:
#            value = float(part)
#            return value
#        except ValueError:
#            continue
#    return None

def read_file_into_array(file_path):
    print("Reading file: " + file_path)
    lines = []
    with open(file_path, 'r') as file:
      lines = [line.strip() for line in file]
#       lines = file.readlines()
#   print("lines: " , lines)
    return lines


#alue_names = ['WBC', 'RBC', 'Hemoglobin', 'Hematocrit', 'Platelets', 'Glucose', 'Albumin']
value_names_file = './blood_report1.values'
value_names      = read_file_into_array(value_names_file)
#rint("Value_names: ", value_names)
#for string in value_names:
#    print("Name:" + string + ".")

if (len(sys.argv) < 2):
    print("   example:  python .\blood_report1.py 'c:/Users/bruce/Documents/Bruce/LabCorp_2024_10a.pdf'")
    exit(0)
    
pdf_path = sys.argv[1]

#df_path = 'C:/Users/bruce/Documents/Bruce/LabCorp_2024_09a.pdf'
print("Parsing: " + pdf_path)

m = parse_labcorp_report(pdf_path, value_names)
#rint("Results: " , m)
#for key in m:
#    if (m[key]):
#        print(key + ' : ' + m[key])

m['age']       = '66'
m['hsCRP']     = '0.2'
m['CystatinC'] = '1.14'
m['SHGB']      = '73'
m['Vitamin D'] = '53'
m['GGT']       = '13'
m['ApoA1']     = '189'
m['urea']      = str(float(m['BUN']) * 0.357)


#https://www.longevity-tools.com/levine-pheno-age#?S-albumin=4.6&S-creatinine=80&S-glucose=92&S-hsCRP=0.55&LYM=32.5&MCV=86&RDW=13.8&S-ALP=45&WBC=4.5&age=42

url1  = 'https://www.longevity-tools.com/levine-pheno-age#?'
url1 += 'S-albumin='     + m['Albumin']
url1 += '&S-creatinine=' + m['Creatinine']
url1 += '&S-glucose='    + m['Glucose']
url1 += '&S-hsCRP='      + m['hsCRP']
url1 += '&LYM='          + m['Lymphs']
url1 += '&MCV='          + m['MCV']
url1 += '&RDW='          + m['RDW']
url1 += '&S-ALP='        + m['Alkaline Phosphatase']
url1 += '&WBC='          + m['WBC']
url1 += '&age='          + m['age']
print(url1)

url2  = 'https://www.longevity-tools.com/humanitys-bortz-blood-age#?'
url2 += 'age=' + m['age'] + '_years'
url2 += '&S-albumin=' + m['Albumin'] + '_g%2FdL'
url2 += '&S-ALP=' + m['Alkaline Phosphatase'] + '_IU%2FL'
url2 += '&S-urea=' + m['urea'] + '_mmol%2FL'
url2 += '&S-cholesterol=' + m['Cholesterol, Total'] + '_mg%2FdL'
url2 += '&S-creatinine=' + m['Creatinine'] + '_mg%2FdL'
url2 += '&S-cystatin-C=' + m['CystatinC'] + '_mg%2FL'
url2 += '&B-HbA1c=' + m['Hemoglobin A1c'] + '_%25'
url2 += '&S-hsCRP=' + m['hsCRP'] + '_mg%2FL'
url2 += '&S-GGT=' + m['GGT'] + '_IU%2FL'
url2 += '&RBC=' + m['RBC'] + '_x10%5E12%2FL'
url2 += '&MCV=' + m['MCV'] + '_fL'
url2 += '&RDW=' + m['RDW'] + '_%25'
url2 += '&MONOabs=' + m['Monocytes(Absolute)'] + '_x10%5E9%2FL'
url2 += '&NEUabs=' + m['Neutrophils (Absolute)'] + '_x10%5E9%2FL'
url2 += '&LYM=' + m['Lymphs'] + '_%25'
url2 += '&S-ALT=' + m['ALT (SGPT)'] + '_IU%2FL'
url2 += '&S-SHBG=' + m['SHGB'] + '_nmol%2FL'
url2 += '&S-25-OH-D=' + m['Vitamin D'] + '_ng%2FmL'
url2 += '&S-glucose=' + m['Glucose'] + '_mg%2FdL'
url2 += '&MCH=' + m['MCH'] + '_pg'
url2 += '&S-ApoA1=' + m['ApoA1'] + '_mg%2FdL'

print(url2)

#https://www.longevity-tools.com/humanitys-bortz-blood-age#?age=42_years&S-albumin=4.6_g%2FdL&S-ALP=45_IU%2FL&S-urea=4.62_mmol%2FL&S-cholesterol=4.17_mmol%2FL&S-creatinine=80_%C2%B5mol%2FL&S-cystatin-C=1.01_mg%2FL&B-HbA1c=5.2_%25&S-hsCRP=0.55_mg%2FL&S-GGT=13.25_IU%2FL&RBC=4.8_x10%5E12%2FL&MCV=86_fL&RDW=13.8_%25&MONOabs=0.34_x10%5E9%2FL&NEUabs=3.79_x10%5E9%2FL&LYM=32.5_%25&S-ALT=18_IU%2FL&S-SHBG=57.22_nmol%2FL&S-25-OH-D=24.91_ng%2FmL&S-glucose=92_mg%2FdL&MCH=30.4_pg&S-ApoA1=1.65_g%2FL

#https://www.longevity-tools.com/humanitys-bortz-blood-age#?age=66_years&S-albumin=4.6_g%2FdL&S-ALP=67_IU%2FL&S-urea=12.852_mmol%2FL&S-cholesterol=116_mg%2FdL&S-creatinine=1.31_mg%2FdL&S-cystatin-C=1.14_mg%2FL&B-HbA1c=5.0_%25&S-hsCRP=0.2_mg%2FL&S-GGT=13_IU%2FL&RBC=4.31_x10%5E12%2FL&MCV=101_fL&RDW=13.1_%25&MONOabs=1.1_x10%5E9%2FL&NEUabs=3.1_x10%5E9%2FL&LYM=34_%25&S-ALT=62_IU%2FL&S-SHBG=73_nmol%2FL&S-25-OH-D=53_ng%2FmL&S-glucose=96_mg%2FdL&MCH=31.8_pg&S-ApoA1=189_mg%2FdL
