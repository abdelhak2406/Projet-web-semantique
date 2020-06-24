import csv

with open ("symptomes.csv", 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Symptomes'])
    filewriter.writerow(['fièvre'])
    filewriter.writerow(['toux sèche'])
    filewriter.writerow(['fatigue'])
    filewriter.writerow(['courbatures'])
    filewriter.writerow(['congestion nasale'])
    filewriter.writerow(['écoulement nasal'])
    filewriter.writerow(['maux de gorge'])
    filewriter.writerow(['diarhée'])
    filewriter.writerow(['détresse respiratoire'])