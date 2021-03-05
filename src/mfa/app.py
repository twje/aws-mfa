import uuid
import json
import logging
from . import util


def setup_logger(level):    
    logging.basicConfig(
        format="time: %(asctime)s, module: %(name)s, line: %(lineno)s, level: %(levelname)s, Msg: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=getattr(logging, level.upper()))


class AWSMixin:
    def set_config(self, profile_name, config, value):
        clazz_name = type(self).__name__.lower()
        try:
            stdout, _, _ = util.run(f"aws configure set {config} {value} --profile {profile_name}")
        except Exception as e:
            raise Exception(f"Unable to set config {config} in AWS {clazz_name}") from e


    def get_config(self, profile_name, config):
        clazz_name = type(self).__name__.lower()
        try:
            stdout, _, _ = util.run(f"aws configure get {config} --profile {profile_name}")
        except Exception as e:
            raise Exception("Unable to get config {config} from AWS {clazz_name}") from e
        
        return stdout


class AWSConfig(AWSMixin):
    def __init__(self, profile_name):
        self.profile_name = profile_name            

    def create(self, aws_expiration, region, output):
        self.set_config(self.profile_name, "aws_expiration", aws_expiration)
        self.set_config(self.profile_name, "region", region)
        self.set_config(self.profile_name, "output", output)
    
    @property
    def mfa_serial(self):
        return self.get_config(self.profile_name, "mfa_serial")

    @property
    def role_arn(self):
        return self.get_config(self.profile_name, "role_arn")

    @property
    def source_profile(self):
        return self.get_config(self.profile_name, "source_profile")

    @property
    def region(self):
        return self.get_config(self.profile_name, "region")

    @property
    def output(self):
        return self.get_config(self.profile_name, "output")


class AWSCredentials(AWSMixin):
    def __init__(self, profile_name):
        self.profile_name = profile_name

    def create(self, aws_access_key_id, aws_secret_access_key, aws_session_token):
        self.set_config(self.profile_name, "aws_access_key_id", aws_access_key_id)
        self.set_config(self.profile_name, "aws_secret_access_key", aws_secret_access_key)
        self.set_config(self.profile_name, "aws_session_token", aws_session_token)


class AWSProfile:
    def __init__(self, profile_name):
        self.config = AWSConfig(profile_name)

    @property
    def mfa_serial(self):
        return self.config.mfa_serial

    @property
    def role_arn(self):
        return self.config.role_arn

    @property
    def source_profile(self):
        return self.config.source_profile

    def upsert_mfa_session_profile(self, new_profile_name, aws_access_key_id, aws_secret_access_key, aws_session_token, aws_expiration):
        # add or override stanza in .aws/credentials
        AWSCredentials(new_profile_name).create(
            aws_access_key_id, 
            aws_secret_access_key,
            aws_session_token
        )

        # add or override stanza in .aws/config        
        AWSConfig(new_profile_name).create(
            aws_expiration, 
            self.config.region,
            self.config.output,
        )


def create_session(profile_name, temporary_profile_name, duration):
    profile = AWSProfile(profile_name)

    # user input
    mfa = input("Enter MFA: ")
    
    # generate new credentials    
    stdout, _, _ = util.run(f"aws sts assume-role --role-arn {profile.role_arn} --serial-number {profile.mfa_serial} --profile {profile.source_profile} --role-session-name {uuid.uuid4()} --token-code {mfa} --duration-seconds {duration}")
    response = json.loads(stdout)

    # create or update profile
    profile.upsert_mfa_session_profile(
        new_profile_name=temporary_profile_name,
        aws_access_key_id=response["Credentials"]["AccessKeyId"],
        aws_secret_access_key=response["Credentials"]["SecretAccessKey"],
        aws_session_token=response["Credentials"]["SessionToken"],
        aws_expiration=response["Credentials"]["Expiration"],
    )
