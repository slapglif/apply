
from app.models import User
from flask_openid import OpenID
import re, requests, time
from app import app
from app import engine
from app import db_session
from flask import url_for, render_template, flash, g, session, \
        redirect
from flask import request
from .forms import xForm
from mandril import drill
from subprocess import (PIPE, Popen)
import datetime
import json

def timenow():
    mylist = []
    today = datetime.date.today()
    mylist.append(today)
    return mylist[0]

def cmd(command):
  return Popen(command, shell=True, stdout=PIPE)

con = engine.connect()
app.secret_key = 'super secret key'
STEAM_API_KEY = "1A15D2C82402F944CF5625FC011EF14C"
open_id = OpenID(app)
_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = xForm()

    output = render_template('apps/index.html',username=g.user,form=form,admin=None)

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        if g.user:
            output = render_template('apps/req.html',username=g.user,form=form,admin=g.user.admin)
        else:
            output = render_template('apps/index.html',username=g.user,form=form,admin=None)


    flash("errors")
    return output


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = xForm()
    g.user = None
    email = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        if g.user is not None:
            email = g.user.email
        output = render_template('apps/index.html',username=g.user,form=form,email=email)
    else:
        output = render_template('apps/index.html',username=g.user,form=form,email=email)

    if form.ign.data != None:
        g.user.ign = form.ign.data
        g.user.email = form.email.data
        g.user.community = form.community.data
        g.user.age = form.age.data
        g.user.div = request.form.get('div')
        g.user.time = request.form.get('time')
        g.user.skills = request.form.get('skills')
        g.user.bio = request.form.get('bio')
        g.user.stuff = request.form.get('industries')
        g.user.disciplines = request.form.get('disciplines')
        g.user.status = "Pending"
        g.user.voteye = 0
        g.user.voteno = 0
        g.user.voted = "0"
        g.user.flag = 3
        g.user.admin = 0
        now = timenow()
        g.user.date = str(now)


        cs = '10'
        tf2 = '12'
        ins = '86'
        gmod = '59'
        se = '82'
        mc = '71'
        pr = '101'
        ut = '114'
        ark = '119'
        chi = '120'
        xy = None


        drill(g.user.nickname,g.user.email)
        db_session.commit()


        if g.user.div == 'Counter-Strike':
            xy = cs
        if g.user.div == 'Insurgency':
            xy = ins
        if g.user.div == 'Team Fortress 2':
            xy = tf2
        if g.user.div == 'Garrys Mod':
            xy = gmod
        if g.user.div == 'Minecraft':
            xy = mc
        # if g.user.div == 'Space Engineers':
        #     xy = se
        if g.user.div == 'Public Relations':
            xy = pr
        if g.user.div == 'Unturned':
            xy = ut
        if g.user.div == 'ARK':
            xy = ark
        if g.user.div == 'Chivalry':
            xy = chi

        try:
            r = requests.get("http://kc1.freebieservers.com/1/info.php?div=%s&name=%s&steam_id=%s"%(xy,g.user.ign,g.user.steam_id))
            print r
            print r.url
        except:
            print "Server Down"
        output = render_template('apps/success.html',username=g.user,form=form)

    return output


@app.route('/req', methods=['GET', 'POST'])
def req():
    form = xForm()
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

    output = render_template('apps/req.html',username=g.user,form=form)

    return output


@app.route('/success', methods=['GET', 'POST'])
def success():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

    output = render_template('apps/success.html',username=g.user)

    return output


def get_steam_userinfo(steam_id):
    options = {
        'key': STEAM_API_KEY,
        'steamids': steam_id
    }
    url = 'http://api.steampowered.com/ISteamUser/' \
          'GetPlayerSummaries/v0001'

    r = requests.get(url, params=options)
    rv = r.json()
    return rv['response']['players']['player'][0] or {}

@app.route('/login')
@open_id.loginhandler
def login():
    if g.user is not None:
        flash("You already have a team!")
        return redirect(open_id.get_next_url())

    return open_id.try_login('http://steamcommunity.com/openid')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('admin', None)
    return redirect(open_id.get_next_url())


@app.before_request
def before_request():
    g.user = None
    print "test here"
    if 'user_id' in session:
        print session['user_id']
        #g.user = User.query.get(session['user_id'])
    else:
        print "test there"

@open_id.after_login
def create_or_login(response):
    match = _steam_id_re.search(response.identity_url)
    g.user = User.get_or_create(match.group(1))
    steamdata = get_steam_userinfo(g.user.steam_id)
    g.user.nickname = steamdata['personaname']
    for user1 in User.query.filter_by(steam_id=g.user.steam_id):
        g.user.flag = [user1][0].flag
        g.user.admin = [user1][0].admin
        print "user1flag is %s user1admin is %s"%([user1][0].flag,[user1][0].admin)
        # if g.user.steam_id == "76561197966341176" or "STEAM_0:0:3037724":
        #     g.user.admin = 1
        #     g.user.flag = 4


    print "%s is admin %s is flag"%(g.user.admin,g.user.flag)
    db_session.commit()

    session['user_id'] = g.user.user_id
    output = redirect(open_id.get_next_url())
    return output



@app.route('/apps')
def apps():
    form = xForm
    g.user = None
    usl = ulist()
    cnt = 0

    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        admin = g.user.admin
        for us in usl:
            cnt += 1
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=reversed(usl),admin=admin,count=cnt)

    else:
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=reversed(usl),admin=False,count=0)

    return output


def ulist():
    userlist = []
    userlist2 = []
    userlist3 = []
    for user2 in User.query.filter(User.email.isnot(None)):
        userlist2 += [user2]
    for user1 in User.query.filter_by(admin='0'):
        userlist += [user1]

    for user3 in userlist:
        if user3 in userlist2:
            userlist3 += [user3]

    return userlist3


def divusl(xf):
    userlist = []
    userlist2 = []
    userlist3 = []
    for user2 in User.query.filter(User.email.isnot(None)):
        userlist2 += [user2]
    for user1 in User.query.filter_by(admin='0'):
        if [user1][0].div == xf:
            userlist += [user1]

    for user3 in userlist:
        if user3 in userlist2:
            userlist3 += [user3]

        return userlist3

@app.route("/apps/<ap>", methods=['GET', 'POST'])
def ap(ap):
    gogo = None
    form = xForm()
    userlist = []
    userlist2 = []
    userlist3 = []
    admin = None
    usl = None
    mod = None
    div = None
    voted = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        if g.user:
            admin = g.user.admin
            mod = g.user.flag
            div = g.user.div
            voted = g.user.voted
    pplz = User.query.filter_by(steam_id=ap)
    for user in pplz:
        gogo = user

    output = render_template('apps/app.html',username=g.user,form=form,gogo=gogo,admin=admin,mod=mod,div=div,voted=voted)

    if ap in "insurgency":
        usl = divusl('Insurgency')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)
    if ap in "counter-strike":
        usl = divusl('Counter-Strike')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)
    if ap in "minecraft":
        usl = divusl('Minecraft')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)
    # if ap in "space engineers":
    #     usl = divusl('Space Engineers')
    #     output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)
    if ap in "team fortress 2":
        usl = divusl('Team Fortress 2')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)
    if ap in "garrys mod":
        usl = divusl('Garrys Mod')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)
    if ap in "ark":
        usl = divusl('ARK')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)
    if ap in "unturned":
        usl = divusl('Unturned')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)

    if ap in "chivalry":
        usl = divusl('Chivalry')
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)


    if form.search.data:
        x = form.search.data

        for user2 in User.query.filter(User.email.isnot(None)):
            userlist2 += [user2]
        for user1 in User.query.filter_by(admin=None):
            if str(x) in str([user1][0].nickname.encode('ascii', 'ignore').lower()):
                userlist += [user1]

        for user3 in userlist:
            if user3 in userlist2:
                userlist3 += [user3]


        usl = userlist3
        cnt = 0
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)

    if request.form.get("datebtn"):

        xf = request.form.get("datebtn")
        userlist = []
        userlist2 = []
        userlist3 = []
        for user2 in User.query.filter(User.email.isnot(None)):
            userlist2 += [user2]
        for user1 in User.query.filter_by(admin='0'):
            if [user1][0].date == xf:
                userlist += [user1]

        for user3 in userlist:
            if user3 in userlist2:
                userlist3 += [user3]

            usl = userlist3
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)


    if request.form.get("divbtn"):
        xf = request.form.get("divbtn")
        userlist = []
        userlist2 = []
        userlist3 = []
        for user2 in User.query.filter(User.email.isnot(None)):
            userlist2 += [user2]
        for user1 in User.query.filter_by(admin=None):
            if [user1][0].div == xf:
                userlist += [user1]

        for user3 in userlist:
            if user3 in userlist2:
                userlist3 += [user3]

            usl = userlist3

        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)


    if request.form.get("statbtn"):
        sbt = request.form.get("statbtn")

        userlist = []
        userlist2 = []
        userlist3 = []
        for user2 in User.query.filter(User.email.isnot(None)):
            userlist2 += [user2]
        for user1 in User.query.filter_by(admin='0'):
            if [user1][0].status == sbt:
                userlist += [user1]

        for user3 in userlist:
            if user3 in userlist2:
                userlist3 += [user3]

            usl = userlist3

        output = render_template('apps/apps.html',username=g.user,form=form,uslz=usl,mod=mod,div=div,voted=voted)



    if request.form.get('datesort'):
        ds = request.form.get('datesort')
        ulsz = ulist()
        output = render_template('apps/apps.html',username=g.user,form=form,uslz=ulsz,mod=mod,div=div,voted=voted)


    if request.form.get('revbtn'):
        x = request.form.get('revbtn')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].status = "Under Review"
            db_session.commit()
            ulsz = ulist()
            output = render_template('apps/app.html',username=g.user,form=form,uslz=ulsz,gogo=gogo,admin=admin,mod=mod,div=div,voted=voted)
    if request.form.get('aprbtn'):
        x = request.form.get('aprbtn')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].status = "Approved"
            db_session.commit()
            ulsz = ulist()
            output = render_template('apps/app.html',username=g.user,form=form,uslz=ulsz,gogo=gogo,admin=admin,mod=mod,div=div,voted=voted)
    if request.form.get('dnybtn'):
        x = request.form.get('dnybtn')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].status = "Denied"
            db_session.commit()
            ulsz = ulist()
            output = render_template('apps/app.html',username=g.user,form=form,uslz=ulsz,gogo=gogo,admin=admin,mod=mod,div=div,voted=voted)

    if request.form.get('dnyreqbtn'):
        x = request.form.get('dnyreqbtn')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].status = "Denied (Requirements Not Met)"
            db_session.commit()
            ulsz = ulist()
            output = render_template('apps/app.html',username=g.user,form=form,uslz=ulsz,gogo=gogo,admin=admin,mod=mod,div=div,voted=voted)


    if request.form.get('voteyes'):
        x = request.form.get('voteyes')
        voted = g.user.voted
        for user1 in User.query.filter_by(steam_id=x):
            vote = [user1][0].voteye
            if vote == None:
                vote = 0
            vote += 1
            [user1][0].voteye = vote
            voted += [user1][0].nickname
            g.user.voted = voted
            db_session.commit()
            ulsz = ulist()
            output = render_template('apps/app.html',username=g.user,form=form,uslz=ulsz,gogo=gogo,admin=admin,mod=mod,div=div,voted=voted)
    if request.form.get('voteno'):
        x = request.form.get('voteno')
        voted = g.user.voted
        for user1 in User.query.filter_by(steam_id=x):
            vote = [user1][0].voteno
            if vote == None:
                vote = 0
            vote += 1
            [user1][0].voteno = vote
            voted += [user1][0].nickname
            g.user.voted = voted
            db_session.commit()
            ulsz = ulist()
            output = render_template('apps/app.html',username=g.user,form=form,uslz=ulsz,gogo=gogo,admin=admin,mod=mod,div=div,voted=voted)


    return output



def admusl():
    userlist2 = []
    for user2 in User.query.filter(User.steam_id.isnot(None)):
        userlist2 += [user2]
    return userlist2

def uslfilter(usl, x):
    userlist2 = []
    for user2 in usl:
        if str(x) in str([user2][0].nickname.encode('ascii', 'ignore').lower()):
             userlist2 += [user2]
    return userlist2

@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin/users', methods=['GET', 'POST'])
@app.route('/admin/users/search', methods=['GET', 'POST'])
def users():
    
    form = xForm(request.form)
    g.user = None

    usl = admusl()
    usl.reverse()
    
    if (request.path == '/admin/users/search'):
        session['sfilter'] = ''

    if (not request.form.get('search')) and (session.has_key('sfilter')): # if it's not a search, reset the usl
       sf = session['sfilter']
       if (len(sf) > 0):
           usl = uslfilter(usl, sf)

    admin = None

    cat = ["Team Fortress 2","Insurgency","Counter-Strike","Garrys Mod","Minecraft","Space Engineers"]
    cat2 = ["L1","L2","L4","JO","Officer","ADL"]
    form.dd1.choices = [(x,x) for x in cat]


    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        admin = g.user.admin

        output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)
    else:
        output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=False,cat=cat,cat2=cat2)



    if request.form.get('Inputs'):
        div = request.form.get('Inputs')
        for user1 in User.query.filter_by(steam_id=div.split('/')[0]):
            [user1][0].div = div.rsplit('/')[1]
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2,div=[user1][0].div)

    if request.form.get('Inputs2'):
        rnk = request.form.get('Inputs2')
        for user1 in User.query.filter_by(steam_id=rnk.split('/')[0]):
            [user1][0].rank = rnk.rsplit('/')[1]
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2,div=[user1][0].div)



    if request.form.get('modbtn'):
        x = request.form.get('modbtn')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].flag = 4
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)
    if request.form.get('rmmbtn'):
        x = request.form.get('rmmbtn')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].flag = 3
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)
    if request.form.get('adadm'):
        x = request.form.get('adadm')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].admin = 1
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)
    if request.form.get('rmadm'):
        x = request.form.get('rmadm')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].admin = 0
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)

    if request.form.get("divbtn"):
        xf = request.form.get("divbtn")
        userlist = []
        userlist2 = []
        userlist3 = []
        for user2 in User.query.filter_by(div=xf):
                userlist2 += [user2]
        if xf == 'None':
            for user2 in User.query.filter_by(div=None):
                userlist2 += [user2]

        usl = userlist2
        output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)

    if request.form.get('advt'):
        x = request.form.get('advt')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].vflag = 1
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)

    if request.form.get('rmvt'):
        x = request.form.get('rmvt')
        for user1 in User.query.filter_by(steam_id=x):
            [user1][0].vflag = 0
            db_session.commit()

            output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)

    if request.form.get('search'):
        x = request.form.get('search')
        usl = uslfilter(usl, x)

        session['sfilter'] = x
        output = render_template('apps/users.html',username=g.user,form=form,uslz=usl,admin=admin,cat=cat,cat2=cat2)

    return output




@app.route("/users/<op>", methods=['GET', 'POST'])
def op(op):
    gogo = None
    form = xForm()
    userlist = []
    userlist2 = []
    userlist3 = []
    admin = None
    usl = None
    mod = None
    div = None
    cat = ["Team Fortress 2","Insurgency","Counter-Strike","Garrys Mod","Minecraft","Space Engineers",'Battlefield','Public Relations']
    cat2 = ["L1","L2","L4","JO","Officer","ADL"]
    form.dd1.choices = [(x,x) for x in cat]
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        if g.user:
            admin = g.user.admin
            mod = g.user.flag
            div = g.user.div
    pplz = User.query.filter_by(steam_id=op)
    for user in pplz:
        gogo = user

    output = render_template('apps/users.html',username=g.user,form=form,gogo=gogo,admin=admin,mod=mod,div=div,voted=g.user.voted,cat=cat,cat2=cat2)

    return output


@app.route('/roster', methods=['GET', 'POST'])
@app.route('/roster/search', methods=['GET', 'POST'])
def roster():
    form = xForm(request.form)
    g.user = None
    usl = admusl()
    admin = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])
        admin = g.user.admin
        output = render_template('apps/roster.html',username=g.user,form=form,uslz=reversed(usl),admin=admin)
    else:
        output = render_template('apps/roster.html',username=g.user,form=form,uslz=reversed(usl),admin=False)
    return output



@app.route("/home/")
def home():

    output = render_template('homepage/index.html')
    return output




@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
