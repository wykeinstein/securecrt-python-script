# $language = "Python"
# $interface = "1.0"

import SecureCRT
import os,sys,time,uuid,socket
import re
#get the current tab
tab=crt.GetScriptTab()
tab.Screen.IgnoreEscape=True
tab.Screen.Synchronous=True

#get the prompt
row=tab.Screen.CurrentRow
prompt=tab.Screen.Get(row,0,row,tab.Screen.CurrentColumn-1).strip()


#get the logfilename
logfilename_prefix=prompt.strip("~#[] ")
script_dir=os.path.dirname(crt.ScriptFullName)
tab.Session.LogFileName=script_dir+"/log/"+logfilename_prefix+"%Y%M%D%%h%m%s.log"

session = crt.Session

def get_file_content(tab, path):
	tab.Screen.Send("cat " + path +  "\r\n")
	tab.Screen.WaitForString("cat " + path)
	file_content = ""
	while True:
		result = tab.Screen.WaitForStrings(["\n", prompt])
		if result == 2:
			break
		screenrow = tab.Screen.CurrentRow - 1
		readline = tab.Screen.Get(screenrow, 1, screenrow, 40)
		file_content += readline + "\n"
	return file_content

def get_ip_list(string):
	ip_pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
	return re.findall(ip_pattern, string)



def main():

	input=crt.Dialog.Prompt("请依次输入包含ip地址的文件路径、ssh账户、ssh密码(用英文逗号分隔开此)：").strip()
	ssh_user=input.split(",")[1].strip()
	ssh_passwd=input.split(",")[2].strip()
	ip_file=input.split(",")[0].strip()
	file_content = get_file_content(tab, ip_file)
	ip_list = get_ip_list(file_content)
	for ip in ip_list:
		tab.Screen.Synchronous=True
		tab.Screen.Send("ssh-copy-id " + ssh_user + "@" + ip + "\n")
		index=tab.Screen.WaitForStrings(["Are you sure you want to continue connecting",
										"WARNING: All keys were skipped because they already exist on the remote system",
										"password","Password"],
										30000)
		if index==1:
			tab.Screen.Send("yes"+"\n")
			tab.Screen.WaitForStrings(["password","Password"],30000)
			tab.Screen.Send(ssh_passwd+"\n")
			tab.Screen.WaitForStrings(prompt,30000)
		elif index == 2:
			continue
		else:
			tab.Screen.Send(ssh_passwd+"\n")
			tab.Screen.WaitForStrings(prompt,30000)

main()





# for host in open("/Users/jason/99cloud_synologydrive/deployment_file/work/ssh_login/hosts","r"):
#	tab.Screen.Synchronous=True
#	tab.Screen.Send("ssh-copy-id "+ssh_user+"@"+host)
#	index=tab.Screen.WaitForStrings(["Are you sure you want to continue connecting","password","Password"],30000)
#	if index==1:
#		tab.Screen.Send("yes"+"\n")
#		tab.Screen.WaitForStrings(["password","Password"],30000)
#		tab.Screen.Send(ssh_passwd+"\n")
#		tab.Screen.WaitForStrings(prompt,30000)
#	else:
#		tab.Screen.Send(ssh_passwd+"\n")
#		tab.Screen.WaitForStrings(prompt,30000)
