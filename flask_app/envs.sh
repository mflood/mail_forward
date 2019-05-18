# adds required environment variables
# to use, run:
#
#   source envs.sh
#   set | grep MF_
export MF_MAILGUN_API_KEY='SOMETHING'
export MF_MAILGUN_DOMAIN='sandbox1111111'
export MF_MANDRILL_API_KEY='aaaaaaaaa-zzzzzzz'

# choose one
export MF_DEFAULT_PROVIDER='mailgun'
#export MF_DEFAULT_PROVIDER='mandrill'
#export MF_DEFAULT_PROVIDER='noop'
