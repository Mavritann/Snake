file = open("leaders.txt", "a")
file.write("poka\n")
file.close()

file = open("leaders.txt", "a")
file.write("pora\n")
file.close()

file = open("leaders.txt", "a")
file.write("domoi")
file.close()


file = open("leaders.txt", "r")
str1 = file.read()
file.close()
print(str1)
