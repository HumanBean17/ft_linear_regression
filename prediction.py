import csv
import sys

def predict(mileage, t0, t1):
    return t0 + (t1 * mileage)

if __name__ == '__main__':
    try:
        with open('coef.csv', "r") as f:
            reader = csv.DictReader(f)
            coef = list(reader)[0]
            t0 = float(coef['t0'])
            t1 = float(coef['t1'])
    except Exception:
        sys.exit("Error: problem with file")

    mileage = 0
    for arg in sys.argv:
        try:
            if arg != "prediction.py":
                mileage = float(arg)
                if mileage < 0:
                    print("Error")
                    sys.exit(-1)
                break
        except Exception as e:
            print("Error")
            sys.exit(-1)    
    print(predict(mileage, t0, t1))