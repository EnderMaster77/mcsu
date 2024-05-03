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
        download_jar(get_latest_papermc_version(
            args.version, args.releasechannel))
    elif args.servertype == "vanilla":
        print("vanilla")
    elif args.servertype == "fabric":
        print("fabric")
    elif args.servertype == "forge":
        print("forge")
    else:
        print("Server type not found!")
        return ()


def get_latest_build_papermc(data={}, releasechannel="default"):
    latest_build = None
    for build in data['builds']:
        if build['channel'] == releasechannel:
            latest_build = build
    if latest_build is None:
        print(f"Build for release channel '{
              releasechannel}' not found. Exiting.")
        quit()
    return latest_build


def get_latest_papermc_version(version="1.19.2", releasechannel="default"):
    url = f"https://papermc.io/api/v2/projects/paper/versions/{version}/builds"
    response = requests.get(url)
    data = response.json()
    try:
        latest_build = get_latest_build_papermc(data, releasechannel)
        latest_build_num = latest_build['build']
        print(f"Release Channel: {latest_build['channel']}")
        download_url = f"https://api.papermc.io/v2/projects/paper/versions/{
            version}/builds/{latest_build_num}/downloads/paper-{version}-{latest_build_num}.jar"
        return download_url
    except KeyError:  # Detect if channel or version is incorrect.
        return


def download_jar(url=""):
    if url != "" and url is not None:
        print(f"downloading jar from: {url}")
    else:
        print("Download URL not found! Try changing the minecraft version.")
        return
    query_params = {"downloadformat": "jar"}
    response = requests.get(url, params=query_params)
    if response.status_code == 200:
        print("Download Succesful!")
        with open("server.jar", mode="wb") as file:
            file.write(response.content)

    else:
        print(f"Download unsucessful, {response.status_code} error.")


main()
