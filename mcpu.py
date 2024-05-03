#!/usr/bin/env python3
import argparse
import requests
import json


def main():
    # Parser  Setup.
    parser = argparse.ArgumentParser(
        description="Command line util to make and manage minecraft servers.")
    parser.add_argument('-v', '--version')
    parser.add_argument('-rc', '--releasechannel', default='default')
    parser.add_argument('-s', '--servertype')
    args = parser.parse_args()

    if args.version is None:
        print("Please set a version!")
        return
    else:
        print("Version Selected:", args.version)
    if args.servertype == "paper":
        dl_link = get_latest_papermc_version(args.version, args.releasechannel)
        if dl_link is not None:
            print(f"downloading jar from: {dl_link}")
            download_jar(dl_link)
        else:
            print(
                "Download failed! You may have incorrectly typed the version or release channel.")
    elif args.servertype == "vanilla":
        print("vanilla")
    elif args.servertype == "fabric":
        print("fabric")
    elif args.servertype == "forge":
        print("forge")
    else:
        print("Server type not found!")
        return ()


def get_latest_papermc_version(version="1.19.2", releasechannel="default"):
    url = f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds"
    response = requests.get(url)
    data = response.json()

    try:
        latest_build = None
        for build in data['builds']:
            if build['channel'] == releasechannel:
                latest_build = build
        latest_build_num = latest_build['build']
        print(latest_build['channel'])
        download_url = f"https://api.papermc.io/v2/projects/paper/versions/{
            version}/builds/{latest_build_num}/downloads/paper-{version}-{latest_build_num}.jar"
        return download_url
    except KeyError:  # Detect if channel or version is incorrect.
        return


def download_jar(url=""):
    query_params = {"downloadformat": "jar"}
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        print("Download Succesful!")
        with open("server.jar", mode="wb") as file:
            file.write(response.content)

    else:
        print(f"Download unsucessful, {response.status_code} error.")


main()
