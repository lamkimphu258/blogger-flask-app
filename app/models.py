from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login, app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.TIMESTAMP, index=True, default=datetime.now)

    def __repr__(self):
        return f'<Post {self.body}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255))
    timestamp = db.Column(db.TIMESTAMP, index=True, default=datetime.now)
    post_id = db.Column(db.Integer, ForeignKey('post.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.cli.command('seed_db')
def seed_db():
    seed_post()
    seed_user()
    seed_comment()


def seed_user():
    user1 = User(firstname='John', lastname='Doe', email='johndoe@email.com')
    user1.set_password('password')
    db.session.add(user1)

    user2 = User(firstname='Jane', lastname='Doe', email='janedoe@email.com')
    user2.set_password('password')
    db.session.add(user2)

    db.session.commit()
    print('Users seeded!')


def seed_comment():
    comment1 = Comment(value='This is an great article', user_id=1, post_id=1)
    db.session.add(comment1)
    comment2 = Comment(value='Your article is awesome', user_id=2, post_id=1)
    db.session.add(comment2)
    comment3 = Comment(value='Terrific article', user_id=1, post_id=2)
    db.session.add(comment3)
    comment4 = Comment(value='This article is bad. Waste my time.', user_id=2, post_id=2)
    db.session.add(comment4)

    db.session.commit()
    print('Comments seeded!')


def seed_post():
    post1 = Post(title='What is Authentication?',
                 body='Definition: Authentication is the process of recognizing a user’s identity. It is the '
                      'mechanism of associating an incoming request with a set of identifying credentials. The '
                      'credentials provided are compared to those on a file in a database of the authorized user’s '
                      'information on a local operating system or within an authentication server. Description: '
                      'The authentication process always runs at the start of the application, before the '
                      'permission and throttling checks occur, and before any other code is allowed to proceed. '
                      'Different systems may require different types of credentials to ascertain a user’s '
                      'identity. The credential often takes the form of a password, which is a secret and known '
                      'only to the individual and the system. Three categories in which someone may be '
                      'authenticated are: something the user knows, something the user is, and something the user '
                      'has.Authentication process can be described in two distinct phases - identification and '
                      'actual authentication. Identification phase provides a user identity to the security '
                      'system. This identity is provided in the form of a user ID. The security system will search '
                      'all the abstract objects that it knows and find the specific one of which the actual user '
                      'is currently applying. Once this is done, the user has been identified. The fact that the '
                      'user claims does not necessarily mean that this is true. An actual user can be mapped to '
                      'other abstract user object in the system, and therefore be granted rights and permissions '
                      'to the user and user must give evidence to prove his identity to the system. The process of '
                      'determining claimed user identity by checking user-provided evidence is called '
                      'authentication and the evidence which is provided by the user during process of '
                      'authentication is called a credential.',
                 timestamp=datetime(2021, 1, 26, 12, 16, 30)
                 )
    db.session.add(post1)

    post2 = Post(title='What is Authorization?',
                 body='Definition: Authorization is a security mechanism to determine access levels or '
                      'user/client privileges related to system resources including files, services, '
                      'computer programs, data and application features. This is the process of granting or '
                      'denying access to a network resource which allows the user access to various resources '
                      'based on the user\'s identity. Description: Most web security systems are based on a '
                      'two-step process. The first step is authentication, which ensures about the user '
                      'identity and the second stage is authorization, which allows the user to access the '
                      'various resources based on the user\'s identity. Modern operating systems depend on '
                      'effectively designed authorization processes to facilitate application deployment and '
                      'management. Key factors contain user type, number and credentials, requiring '
                      'verification and related actions and roles. Access control in computer systems and '
                      'networks relies on access policies and it is divided into two phases: 1) Policy '
                      'definition phase where access is authorized. 2) Policy enforcement phase where access '
                      'requests are permitted or not permitted. Thus authorization is the function of the '
                      'policy definition phase which precedes the policy enforcement phase where access '
                      'requests are permitted or not permitted based on the previously defined authorizations. '
                      'Access control also uses authentication to check the identity of consumers. When a '
                      'consumer attempts to access a resource, the access control process investigates that '
                      'the consumer has been authorized to use that resource. Authorization services are '
                      'implemented by the Security Server which can control access at the level of individual '
                      'files or programs.',
                 timestamp=datetime(2021, 1, 22, 11, 16, 30)
                 )
    db.session.add(post2)

    db.session.commit()
    print('Posts seeded!')
