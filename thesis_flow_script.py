import zipfile
import os, sys
import shutil
import glob

decompile_path = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\dex2jar-2.0")
normal_app_path = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\Malware_APP")
Malware_app_path = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\Malware_APP")
jarfile_save_path = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\jarfile")
ExtractionOfZip_path = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\ExtractionOfZip")
JAVAStoration_path = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\store_each_java")
ToDoJAD_path = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\to_do_jad")
NormalFinalJavaPath = ("C:\\Users\\islab718A\\Desktop\\PARFORTHESIS\\final_all_java_malware")

print "copy normal_apk to folder..."
for foldername in os.listdir(normal_app_path): 
	for filename in os.listdir(normal_app_path+"\\"+foldername): 
		if os.path.exists(JAVAStoration_path+"\\"+filename.replace(".apk", "")):
			continue
		else:
			#copy to dex2jar part
			src = (normal_app_path+"\\"+foldername+"\\"+filename)
			dst = (decompile_path)
			shutil.copy2(src, dst)
			#execute dex2jar part
			os.chdir(decompile_path)
			os.system("d2j-dex2jar.bat "+filename)
			os.remove(filename)  
			jar_name = filename.replace(".apk", "-dex2jar.jar")
			jar2zip_name = jar_name.replace(".jar", ".zip")
			try:
				os.rename(decompile_path + "\\" + jar_name, jarfile_save_path + "\\" + jar2zip_name)
			except WindowsError, e:
				continue
			#extract all zip to one folder
			zip_ref = zipfile.ZipFile(jarfile_save_path + "\\" + jar2zip_name, 'r')
			zip_ref.extractall(ExtractionOfZip_path + "\\" + filename.replace(".apk", ""))
			zip_ref.close()
			os.remove(jarfile_save_path + "\\" + jar2zip_name)
			#run through all class in filename folder, then for each using jad
			for root, dirs, files in os.walk(ExtractionOfZip_path + "\\" +filename.replace(".apk", "")):#root is class's path
				for file in files:
					if file.endswith('.class'):
						if not os.path.exists(JAVAStoration_path+"\\"+filename.replace(".apk", "")):
							os.makedirs(JAVAStoration_path+"\\"+filename.replace(".apk", ""))
						o = 0
						while True:
							iu = 0
							if os.path.exists(ToDoJAD_path+"\\"+str(o)+file):
								o = o + 1
							else:
								try:
									os.rename(root+"\\"+file, ToDoJAD_path+"\\"+str(o)+file)
									break
								except WindowsError, e:
									iu = 1
									break
						if iu == 1:
							continue
						os.chdir(ToDoJAD_path)
						g = 0
						while True:
							if os.path.exists(str(o)+file.replace(".class",str(g) + ".java")):
								g = g + 1
							else:
								os.system("jad -p "+str(o)+file+" > "+str(o)+file.replace(".class",str(g) + ".java"))
								break
						k=0
						while True:
							if os.path.exists(JAVAStoration_path + "\\" + filename.replace(".apk", "") + "\\" +str(o)+ file.replace(".class",str(g)+ str(k)+".java")):
								k = k + 1
							else:
								os.rename(str(o)+file.replace(".class",str(g) + ".java"), JAVAStoration_path + "\\" + filename.replace(".apk", "") + "\\" + str(o)+file.replace(".class",str(g)+ str(k)+".java"))
								break
						#os.remove(file)
						os.chdir(decompile_path)##if
			#all java code in one file
			os.chdir(JAVAStoration_path+"\\"+filename.replace(".apk", ""))
			try:
				os.remove(NormalFinalJavaPath+"\\"+ filename.replace(".apk", ".txt"))
			except OSError:
				pass
			with open(NormalFinalJavaPath+"\\"+ filename.replace(".apk", ".txt"), 'w') as outfile:
				for fname in os.listdir(JAVAStoration_path+"\\"+filename.replace(".apk", "")):
					with open(fname) as infile:
						for line in infile:
							if 'Copyright' not in line and 'Jad' not in line and 'options' not in line and '//' not in line:
								outfile.write(line)

print "finish copy normal_apk to folder"
