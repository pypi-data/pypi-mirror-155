import requests, os, re

url = "https://www.findtubes.com/pornstar/"
pattern = r"<li class=\"category\" data-title=\"(\w*\s+?\w*?\w*?\s?)\"><a href=\"\/pornstar\/(\w*-?\w*?-?\w*?)\">(\w*\s?\w*?\s?\w*?)<span class=\"badge text-muted\">(\d*)<\/span><\/a><\/li>"

def GrabPornStars():
    
    sourceCode = requests.get(url).text
    run = True
    lines = ""
    while run == True:
        
        try:
            result = re.search(pattern, sourceCode)
            string = "(<li class=\"category\" data-title=\"" + result.group(1)+ "\"><a href=\"\/pornstar\/" + result.group(2)+ "\">" + result.group(3)+ "<span class=\"badge text-muted\">" + result.group(4)+ "<\/span><\/a><\/li>)"
        except:
            run = False
            print("Propably done!")
            SaveFile(lines)
            return   
        
        try:
            sourceCode = re.sub(string, "", sourceCode)
            print(result.group(1))
            lines += result.group(1) + "\n"
        except:
            run = False
            print("Propably done!")
            SaveFile(lines)
            
    SaveFile(lines)

def SaveFile(_lines):   
    file = open(os.getcwd()+"static/data/pornStarDicitonary_new", "w")
    file.writelines(_lines)
    file.close()
    
    
    
    
if __name__ == "__main__":
    GrabPornStars()