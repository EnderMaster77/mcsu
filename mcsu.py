#!/usr/bin/env python3
import argparse
import requests
import platform


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
        quit()
    else:
        print("Version Selected:", args.version)

    jar_setup(args)  # Downloads the Jar file.
    startup_setup()  # Gives EULA prompt and creates run.sh.


def startup_setup():
    eula_prompt()
    create_run_script()


def create_run_script():
    print("Creating Script.")
    if platform.platform().lower() == "windows":
        print("Windows script creation not supported yet!")
        return
    while True:
        ram = input("RAM (Gigabytes):")
        try:
            ram = int(ram)
            break
        except ValueError:
            print("Please type a whole number.")
    try:
        startsh = open("start.sh", "w")
        startsh.write(f"java -jar -Xmx{ram}G server.jar --nogui")
    except IOError as e:
        print(f"Run script creation failed, Couldn't write to file ({e})")
        return ()
    print("Run script created succesfully.")


def eula_prompt():
    eularesponse = input("Agree to Minecraft Eula? [y/n]")
    while True:
        if eularesponse.lower() == "n":
            print("Did not agree to EULA. Server will not start.")
            break
        elif eularesponse.lower() == "y":
            print("Agreeing to EULA")
            eula = open("eula.txt", "w")
            eula.write("eula=true")
            break
        else:
            eularesponse = input("Agree to Eula? [y/n]")


def jar_setup(args):
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
        quit()


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
