import logging
import grpc
import json

from concurrent.futures import ThreadPoolExecutor
from blackacre_pb2_grpc import BlackacreServicer, add_BlackacreServicer_to_server

def arg_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Blackacre NLP gRPC Server")
    parser.add_argument("-p", "--port", type=int, help="", default=9999)
    parser.add_argument("-r", "--rules", type=str, help="", default="")
    parser.add_argument("-m", "--baseModel", type=str, help="", default="en_core_web_md")
    return parser.parse_args()

def rules(args):
    if args.rules != "":
        with open(args.rules) as f:
            return json.load(f)
    else:
        return []

def logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def server(args):
    server = grpc.server(ThreadPoolExecutor())
    server.add_insecure_port(f'[::]:{args.port}')
    return server

def servicer(server, servicer, opts):
    add_BlackacreServicer_to_server(servicer(rules=opts["rules"]), server)