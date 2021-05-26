from csv import reader

import sys
import matplotlib.pyplot as plt

def load_csv():
    dataset = list()
    filename = None
    i = 0
    error = False
    for arg in sys.argv:
        if arg != "ft_linear_regression.py":
            filename = arg
            break
    try:
        with open(filename, 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if not row: continue
                for column in range(len(row)):
                    try:
                        row[column] = float(row[column].strip())
                    except ValueError:
                        if i == 0: 
                            error = True
                            pass
                        else:
                            print("File validation ERROR")  
                            sys.exit(-1)
                if error is False:       
                    dataset.append(row)
                error = False
                i += 1
    except Exception:
        print("Error: problem with file")
        sys.exit(-1)
    return dataset

def predict(mileage, t0, t1):
    return t0 + (t1 * mileage)

def coefficients_sgd(train, l_rate):
    t0, t1 = mnk(train)
    while True:
        t0_sum_error = 0.0
        t1_sum_error = 0.0
        for row in train:
            mileage = row[0] / 1000.0
            price = row[1] / 1000.0

            yhat = predict(mileage, t0, t1) - price
            t0_sum_error += l_rate * yhat
            t1_sum_error += l_rate * yhat * mileage

        t0_error = t0_sum_error / len(dataset)
        t1_error = t1_sum_error / len(dataset)
        if abs(t0_error) < 0.000001 and abs(t1_error) < 0.000001:
            break

        t0 -= t0_error
        t1 -= t1_error
    return round(t0 * 1000.0, 5), round(t1, 5)

def mnk(dataset: list):
    mileage = []
    price = []
    n = len(dataset)
    for row in dataset:
        mileage.append(row[0])
        price.append(row[1])

    s = sum(price)
    s1 = sum([mileage[i] for i in range(0, n)])
    s2 = sum([(mileage[i]) ** 2 for i in range(0, n)])
    s3 = sum([price[i] * mileage[i] for i in range(0, n)])

    t0 = round((s * s2 - s1 * s3) / (n * s2 - s1 ** 2), 6)
    t1 = round((n * s3 - s1 * s) / (n * s2 - s1 ** 2), 6)
    return t0, t1


if __name__ == '__main__':
    dataset = load_csv()
    mileage_lst = [row[0] for row in dataset]
    price_lst = [row[1] for row in dataset]

    l_rate = 0.0001
    t0, t1 = coefficients_sgd(dataset, l_rate)
    with open('coef.csv', 'w') as f:
            f.write('t0,t1\n')
            f.write(f'{t0},{t1}\n')
    ml = [t0 + t1 * mileage_lst[i] for i in range(len(dataset))]

    plt.rcParams['figure.figsize'] = (12.0, 9.0)
    plt.title('Linear regression')
    plt.xlabel('Km', size=14)
    plt.ylabel('Price', size=14)
    plt.plot(mileage_lst, price_lst, color='b', linestyle=' ', marker='o', label='Data(km,price)')
    plt.plot(mileage_lst, ml, color='r', linewidth=2)
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

