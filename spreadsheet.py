import gspread, time
from InstagramAPI import InstagramAPI
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Followers').sheet1
userindex=2
usernames=[]
InstagramAPI = InstagramAPI('UNAME', 'PWORD')
InstagramAPI.login()
InstagramAPI.getProfileData()

followers = InstagramAPI.getTotalSelfFollowers()
following = InstagramAPI.getTotalSelfFollowings()

for i in following:
    usernames.append(i['username'])

for user in followers:
    if user['username'] in usernames:
        totalposts = len(InstagramAPI.getTotalUserFeed('%d' % user['pk']))
        totalfollowers = len(InstagramAPI.getTotalFollowers('%d' % user['pk']))
        totalfollowing = len(InstagramAPI.getTotalFollowings('%d' % user['pk']))
        print(user)
        print(user['pk'], user['username'], user['full_name'], totalposts, totalfollowers, totalfollowing)
        sheet.update_cell(userindex, 1, '=IMAGE("%s",4,50,50)' % user['profile_pic_url'])
        sheet.update_cell(userindex, 2, '=HYPERLINK("https://www.instagram.com/%s/","%s")' % (user['username'], user['username']))
        sheet.update_cell(userindex, 3, '%s' % user['full_name'])
        sheet.update_cell(userindex, 4, '%s' % totalposts)
        sheet.update_cell(userindex, 5, '%s' % totalfollowers)
        sheet.update_cell(userindex, 6, '%s' % totalfollowing)
        userindex += 1
        time.sleep(1)
    elif user['username'] not in usernames and user['is_private'] is False:
        totalposts = len(InstagramAPI.getTotalUserFeed('%d' % user['pk']))
        totalfollowers = len(InstagramAPI.getTotalFollowers('%d' % user['pk']))
        totalfollowing = len(InstagramAPI.getTotalFollowings('%d' % user['pk']))
        print(user)
        print(user['pk'], user['username'], user['full_name'], totalposts, totalfollowers, totalfollowing)
        sheet.update_cell(userindex, 1, '=IMAGE("%s",4,50,50)' % user['profile_pic_url'])
        sheet.update_cell(userindex, 2, '=HYPERLINK("https://www.instagram.com/%s/","%s")' % (user['username'], user['username']))
        sheet.update_cell(userindex, 3, '%s' % user['full_name'])
        sheet.update_cell(userindex, 4, '%s' % totalposts)
        sheet.update_cell(userindex, 5, '%s' % totalfollowers)
        sheet.update_cell(userindex, 6, '%s' % totalfollowing)
        userindex += 1
        time.sleep(1)
    else:
        print(user['pk'], user['username'], user['full_name'])
        print(user)
        sheet.update_cell(userindex, 1, '=IMAGE("%s",4,50,50)' % user['profile_pic_url'])
        sheet.update_cell(userindex, 2, '=HYPERLINK("https://www.instagram.com/%s/","%s")' % (user['username'],user['username']))
        sheet.update_cell(userindex, 3, '%s' % user['full_name'])
        sheet.update_cell(userindex, 4, '%s' % 'PRIVATE')
        sheet.update_cell(userindex, 5, '%s' % 'PRIVATE')
        sheet.update_cell(userindex, 6, '%s' % 'PRIVATE')
        userindex += 1
        time.sleep(1)