import boto

def get_s3_client():
    conn = boto.connect_s3('AKIARUYJYFCS6I7UCPMD', '4rnhTe7GalZABQrrxj001rMcypffVcl8E/ieIGNJ')
    bucket = conn.get_bucket('gpsurvey')

    return bucket