import re
import pandas as pd
import argparse
import os

parser=argparse.ArgumentParser()
group=parser.add_mutually_exclusive_group()
parser.add_argument("log_file",type=str,help="Name of the file you want to parse.")
group.add_argument("-f","--frontend",action="store_true",help="Used if you want to parse a storm-frontend log file.")
group.add_argument("-b","--backend",action="store_true",help="Used if you want to parse a storm-backend log file.")
args=parser.parse_args()
log_file=args.log_file
if args.frontend:
        log_type="frontend-server"
        input_dir = '/container/logfiles/frontend-server/'
        print("Parsing {} as a frontend log file..".format(log_file))
        log_format = '<Date> <Time> <Pid> - <Level> <Component>: <Content>'#Frontend logformat
elif args.backend:
        log_type="backend-server"
        input_dir = '/container/logfiles/backend-server/'
        print("Parsing {} as a backend log file..".format(log_file))
        log_format = '<Time> - <Level> <Component> - <Content>'#Backend logformat
        
def load_data():
        headers, regex = generate_logformat_regex(log_format)
        return log_to_dataframe(os.path.join(input_dir, log_file), regex, headers, log_format)

def log_to_dataframe(logfile, regex, headers, logformat):
        """ Function to transform log file to dataframe 
        """
        log_messages = []
        linecount = 0
        with open(logfile, 'r') as fin:
            for line in fin.readlines():
                line = re.sub(r'[^\x00-\x7F]+', '<NASCII>', line)
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers, dtype=str)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        file_out=open("results/{}/{}_struct.csv".format(log_type,log_file),"w")
        logdf.to_csv(file_out)
        file_out.close()
        #return logdf
def generate_logformat_regex(logformat):
        """ Function to generate regular expression to split log messages
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', '\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex
        
load_data()        
