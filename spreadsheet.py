import gspread, time
from InstagramAPI import InstagramAPI
from oauth2client.service_account import ServiceAccountCredentials


#gspread_authorize
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

#gspread_sheet
sheet = client.open('Followers').sheet1

#instagram_authorize
igapi = InstagramAPI('paunzz', 'ILoveSandwiches')
igapi.login()
igapi.getProfileData()


cells = list()
userindex=2
usernames=[]
followers = igapi.getTotalSelfFollowers()
following = igapi.getTotalSelfFollowings()


def update(user, userindex):
    totalposts = len(igapi.getTotalUserFeed('%d' % user['pk']))
    totalfollowers = len(igapi.getTotalFollowers('%d' % user['pk']))
    totalfollowing = len(igapi.getTotalFollowings('%d' % user['pk']))
    print(user)
    print(user['pk'], user['username'], user['full_name'], totalposts, totalfollowers, totalfollowing)
    cells.append(gspread.Cell(userindex, 1, '=IMAGE("%s",4,50,50)' % user['profile_pic_url']))
    cells.append(gspread.Cell(userindex, 2, '=HYPERLINK("https://www.instagram.com/%s/","%s")' % (user['username'], user['username'])))
    cells.append(gspread.Cell(userindex, 3, '%s' % user['full_name']))
    cells.append(gspread.Cell(userindex, 4, '%s' % totalposts))
    cells.append(gspread.Cell(userindex, 5, '%s' % totalfollowers))
    cells.append(gspread.Cell(userindex, 6, '%s' % totalfollowing))

def update_private(user, userindex):
    print(user)
    print(user['pk'], user['username'], user['full_name'])
    cells.append(gspread.Cell(userindex, 1, '=IMAGE("%s",4,50,50)' % user['profile_pic_url']))
    cells.append(gspread.Cell(userindex, 2, '=HYPERLINK("https://www.instagram.com/%s/","%s")' % (user['username'], user['username'])))
    cells.append(gspread.Cell(userindex, 3, '%s' % user['full_name']))
    cells.append(gspread.Cell(userindex, 4, '%s' % 'PRIVATE'))
    cells.append(gspread.Cell(userindex, 5, '%s' % 'PRIVATE'))
    cells.append(gspread.Cell(userindex, 6, '%s' % 'PRIVATE'))


for i in following:
    usernames.append(i['username'])

for user in followers:
    if user['username'] in usernames:
        update(user, userindex)
        userindex += 1
        time.sleep(1)
    elif user['username'] not in usernames and user['is_private'] is False:
        update(user, userindex)
        userindex += 1
        time.sleep(1)
    else:
        update_private(user, userindex)
        userindex += 1
        time.sleep(1)
    sheet.update_cells(cells, value_input_option='USER_ENTERED')
    cells.clear()