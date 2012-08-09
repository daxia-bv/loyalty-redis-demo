import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-mg", "--merchantGroupId", type=int, help="Process only for this merchant group id")
parser.add_argument("-profile", "--profileId", type=int, help="Process only for this profile id")

args = parser.parse_args()
merchantGroupId = args.merchantGroupId
profileId = args.profileId