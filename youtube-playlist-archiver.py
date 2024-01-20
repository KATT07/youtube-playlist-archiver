#this is a script to show privated/deleted videos in a playlist
#if needed save it to a file for later viewing of results of the file

import pickle
from googleapiclient.discovery import build

#tutorial for how to get youtube data api v3 developer key
api_key=input("Enter your YouTube DATA API V3 API KEY :")
youtube = build('youtube','v3',developerKey=api_key)
print()

pl_url=input("enter playlist url :")
pl_id=pl_url[38::]

big_data=[]

def scan_new():
    global big_data
    big_data=[]
    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=pl_id,
            maxResults=50,
            pageToken=nextPageToken
        )
        pl_response = pl_request.execute()
        for item in pl_response['items']:
            videoId=item['snippet']['resourceId']['videoId']
            title=item['snippet']['title']
            description=item['snippet']['description']
            LST=[videoId,title,description]
            big_data.append(LST)
            print(title," | found")

        nextPageToken=pl_response.get('nextPageToken')
        if nextPageToken==None:
            break

    pl_no=len(big_data)
    print()
    print("Number of videos detected in playlist =",pl_no)
    count=0
    for i in big_data:
        if i[1]=="Private video" or i[1]=="Deleted video":
            count+=1
            print(count,". ","Private/Deleted videos in scan :",i)

#Keep this file saved somewhere
def write_new():
    if big_data!=[]:
        f=open("big_data.bin",'wb')
        pickle.dump(big_data,f)
        print("Saved items to the file")
    else:
        print("No playlist scanned yet scan a playlist 1st")
    f.close()

def print_big_data():
    f=open('big_data.bin','rb')
    big_data=pickle.load(f)
    count=0
    for i in big_data:
        count+=1
        print(count,". ",i)
    print()
    print("Number of videos detected in big_data =",len(big_data))
    f.close()

def print_big_data_deleted():
    f=open("big_data.bin","rb")
    big_data=pickle.load(f)
    count=0
    print("Private/Deleted videos in big_data.bin :")
    for i in big_data:
        if i[1]=="Private video" or i[1]=="Deleted video" or i[2]=="This video is unavailable.":
            count+=1
            print(count,". ",i)
    f.close()

def print_big_data_deleted_links():
    f=open("big_data.bin","rb")
    big_data=pickle.load(f)
    count=0
    print("Deleted videos links are :")
    for i in big_data:
        if i[1]=="Private video" or i[1]=="Deleted video" or i[2]=="This video is unavailable.":
            count+=1
            print(count,", ",i[1]," - ","https://youtu.be/"+i[0])
    f.close()

def search_big_data():
    f=open("big_data.bin","rb")
    big_data=pickle.load(f)
    print("1.Search Titles")
    print("2.search Description")
    print("3.search Video ID")
    print()
    choice=int(input("Enter choice for search :"))
    search=input("Enter search string :")
    print()
    aa="True"
    if choice==1:
        for i in big_data:
            if search.lower() in i[1].lower():
                print(i[1])
                aa="False"
    elif choice==2:
        for i in big_data:
            if search.lower() in i[2].lower():
                print(i)
                aa="False"
    elif choice==3:
        for i in big_data:
            if search==i[0]:
                print(i)
                aa="False"
    else:
        print("Invalid input")

    if aa=="True":
        print("Not Found")

    f.close()

while True:
    print()
    print('1.Scan a new playlist')
    print('2.Save scanned item to a file (wont work if no scanned items)')
    print('3.Print big_data.bin')
    print("4.Print big_data.bin but only Deleted/Privated videos")
    print("5.Print big_data.bin but only Deleted/Privated videos with links")
    print('6.Search big_data.bin for specific item')
    print("7.Exit program")
    print()
    choice=int(input('Enter choice :'))
    print()
    if choice==1:
        scan_new()
    elif choice==2:
        write_new()
    elif choice==3:
        print_big_data()
    elif choice==4:
        print_big_data_deleted()
    elif choice==5:
        print_big_data_deleted_links()
    elif choice==6:
        search_big_data()
    elif choice==7:
        break
    else:
        print("Invalid choice")

#End of program
