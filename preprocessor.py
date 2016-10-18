def preprocess(filenames):
    new_filenames = []
    print (filenames)

    for filename in filenames:
        input_file = open(filename, "r")
        output_filename = filename.split('.')[0] + ".x"
        output_file = open(output_filename, "w+")
        code = input_file.read()
        r_ini = False
        lines = code.split('\n')
        for line in lines:
            n = line.count(',')
            if "min" in line:
                numbers = line.split('(')[1].split(',')
                numbers[-1] = numbers[-1][:-1]
                if not r_ini:
                    output_file.write("var ")
                output_file.write("r=" + numbers[0] + "\n" + "loop " + str(n) + "\n")
                for num in numbers:
                    output_file.write("if " + "r>" + num + "\n" + "r=" + num + "\n" + "endif" + "\n")
                output_file.write("endloop" + "\n")
                output_file.write(line.split('(')[0][:-3] + "r" + "\n")
                r_ini = True
            elif "max" in line:
                numbers = line.split('(')[1].split(',')
                numbers[-1] = numbers[-1][:-1]
                if not r_ini:
                    output_file.write("var ")
                output_file.write("r=" + numbers[0] + "\n" + "loop " + str(n) + "\n")
                for num in numbers:
                    output_file.write("if " + "r<" + num + "\n" + "r=" + num + "\n" + "endif" + "\n")
                output_file.write("endloop" + "\n")
                output_file.write(line.split('(')[0][:-3] + "r" + "\n")
                r_ini = True
            elif "add" in line:
                numbers = line.split('(')[1].split(',')
                numbers[-1] = numbers[-1][:-1]
                if not r_ini:
                    output_file.write("var ")
                output_file.write("r=0" + "\n" + "loop " + str(n) + "\n")
                for num in numbers:
                    output_file.write("r=r+" + num + "\n")
                output_file.write("endloop" + "\n")
                output_file.write(line.split('(')[0][:-3] + "r" + "\n")
                r_ini = True
            elif "multiply" in line:
                numbers = line.split('(')[1].split(',')
                numbers[-1] = numbers[-1][:-1]
                if not r_ini:
                    output_file.write("var ")
                output_file.write("r=0" + "\n")
                for i in range(1, int(numbers[1]) + 1):
                    output_file.write("r=r+" + numbers[0] + "\n")
                output_file.write("endloop" + "\n")
                output_file.write(line.split('(')[0][:-8] + "r" + "\n")
                r_ini = True
            elif "*" in line:
                numbers = line.split('=')[1].split('*')
                if not r_ini:
                    output_file.write("var ")
                output_file.write("r=0" + "\n")
                for i in range(1, int(numbers[1]) + 1):
                    output_file.write("r=r+" + numbers[0] + "\n")
                output_file.write("endloop" + "\n")
                output_file.write(line.split('=')[0] + "=" + "r" + "\n")
                r_ini = True
            elif "+" in line:
                numbers = line.split('=')[1].split('+')
                if not r_ini:
                    output_file.write("var ")
                output_file.write("r=0" + "\n")
                for num in numbers:
                    output_file.write("r=r+" + num + "\n")
                output_file.write("endloop" + "\n")
                output_file.write(line.split('=')[0] + "=" + "r" + "\n")
                r_ini = True
            else:
                output_file.write(line + "\n")
        output_file.close()
        new_filenames.append(output_filename)
    return new_filenames
