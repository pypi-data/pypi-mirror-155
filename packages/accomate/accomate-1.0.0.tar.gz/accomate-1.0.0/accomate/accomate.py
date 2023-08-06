import subprocess
import os
import json
import sys
import time
import typer

from accomate.utils.config import validate_project_config
from accomate.utils.dns import dns_check

from .aws.route53 import add_dns_record, get_hosted_zone_id, verify_dns_record
from .utils.command import is_installed
from .utils.compose import assign_service_type_tag, compose_down, compose_up, get_containers_on_same_network, restart_containers
from .utils.echo import echo
from .utils.git import clone_repo
from .utils.keys import write_all_the_keys
from .utils.network import find_open_port, get_machine_public_ip
from .utils.nginx import add_lets_encrypt_certificate, restart_nginx, verify_nginx_conf
from .utils.validators import validate_email, validate_enviorment
from .utils.yaml_file import read_yaml_file, write_yaml_file
from .utils.passwords import generate_django_secret_key, generate_random_password
import dotenv
from .utils.store import generate_store_app_id, generate_store_app_key
from .aws import s3
import randomname

app = typer.Typer()

USER = os.environ.get("USER")

# [DEFAULT]
accoladez_config_path = f"/home/{USER}/accoladez/config.yaml"
accoladez_config = None
accoladez_base_path = f"/home/{USER}/accoladez"
accoladez_base_store_path = f"/home/{USER}/accoladez/stores"
accoladez_base_domain = "itdaycloud.com"
store_service_images = {
    "2.0.0": "042826358439.dkr.ecr.us-east-1.amazonaws.com/accoladez-store:2.0.0",
    "2.0.1": "042826358439.dkr.ecr.us-east-1.amazonaws.com/accoladez-store:2.0.1",
    "2.0.2": "042826358439.dkr.ecr.us-east-1.amazonaws.com/accoladez-store:2.0.2"
}

auth_service_images = {
    "1.0.0": "042826358439.dkr.ecr.us-east-1.amazonaws.com/accoladez-auth:1.0.0",
    "2.0.0": "042826358439.dkr.ecr.us-east-1.amazonaws.com/accoladez-auth:2.0.0",
    "2.0.1": "042826358439.dkr.ecr.us-east-1.amazonaws.com/accoladez-auth:2.0.1",
    "2.0.2": "042826358439.dkr.ecr.us-east-1.amazonaws.com/accoladez-auth:2.0.2",
}
base_nginx_path = f"/home/{USER}/accoladez/nginx/conf"

absolute_package_path = os.path.dirname(os.path.abspath(__file__))
machine_ip_address = get_machine_public_ip()
hosted_zone_id = None

if not os.path.exists(accoladez_base_path):
    action = sys.argv[1] if len(sys.argv) > 1 else False

    if action != "install":
        echo("🚫 Accomate is not installed.")
        echo("Run `python cli.py install` to install .")
        sys.exit(1)
else:
    try:
        accoladez_config = read_yaml_file(accoladez_config_path)
        if accoladez_config is not None:
            accoladez_base_store_path = accoladez_config['base_store_path']
            os.environ.setdefault("GITHUB_PERSONAL_TOKEN",
                                  accoladez_config['github_personal_token'])
            store_service_images = accoladez_config['store_service_images']
            auth_service_images = accoladez_config['auth_service_images']
            accoladez_base_domain = accoladez_config['base_domain']
            hosted_zone_id = get_hosted_zone_id(accoladez_base_domain)

        else:
            echo("Configuration is not defined!!")
            exit(code=901)
    except FileNotFoundError as _:
        echo("🚀 Reinstall .")
        echo("Running `python cli.py install` to install .")
    except Exception as _:
        echo("Something went wrong ☹️.")
        exit(code=901)


@app.command()
def install():
    try:
        # Setting up Accoladez to start building stores

        if not os.path.exists(accoladez_base_path):
            os.mkdir(f"/home/{USER}/accoladez")
        else:
            reinstall = input(
                "🚫 Accomate is already installed. Do you want to reinstall? (y/n) ")
            if reinstall == "y":
                echo("🚀 Reinstalling .")
                subprocess.run(["rm", "-rf", accoladez_base_path])
                os.mkdir(f"/home/{USER}/accoladez")
            else:
                echo("🚫 Exiting.")
                exit(code=901)

        # Install Nginx if not available
        if is_installed("nginx"):
            echo("Nginx is already installed.")
        else:
            echo("Installing Nginx")
            subprocess.call(["sudo", "apt-get", "install", "nginx"])

        # Configure Nginx
        echo("Configuring Nginx")

        nginx_conf = os.path.join(absolute_package_path, "conf", "nginx.conf")

        # print(nginx_conf)

        with open(nginx_conf, "r+") as f:
            # Update user variable in nginx_conf
            file = f.read()
            file = file.replace("#user#", USER)
            f.truncate(0)
            f.seek(0)
            f.write(file)

        subprocess.call(
            ["sudo", "cp", nginx_conf, "/etc/nginx/nginx.conf"])
        restart_nginx()

        # Install Docker if not available
        if is_installed("docker"):
            echo("Docker is already installed.")
        else:
            echo("Installing Docker")
            subprocess.call(["sudo", "sh", "scripts/docker-install.sh"])

        # Install Docker Compose if not available
        if is_installed("docker compose", "version"):
            echo("Docker Compose is already installed.")
        else:
            echo("Installing Docker Compose")
            subprocess.call(["sudo", "sh", "docker-compose-install.sh"])

        if is_installed("certbot", "--version"):
            echo("Certbot is already installed.")
        else:
            subprocess.call(["sudo", "apt-get", "install", "certbot"])
            subprocess.call(
                ['sudo', 'apt', 'install', 'python3-certbot-nginx'])

        # Install AWS CLI if not available
        if is_installed("aws", "--version"):
            echo("AWS CLI is already installed.")
        else:
            echo("Installing AWS CLI")
            subprocess.call(["sudo", "apt-get", "install", "awscli"])

        echo("Github Personal Token least required privileges are: 'private_repo', 'repo', 'org:read'")
        GITHUB_PERSONAL_TOKEN = str(
            input("Enter your Github personal token: "))

        config = {
            "github_personal_token": GITHUB_PERSONAL_TOKEN,
            "base_domain": accoladez_base_domain,
            "base_store_path": accoladez_base_store_path,
            "store_service_images": store_service_images,
            "auth_service_images": auth_service_images,
        }

        write_yaml_file(accoladez_config_path, config)

        echo("🚀 Accomate setup is done, you can now start building stores")

        echo("Happy Accoladezing! 😎")
    except typer.Abort as _:
        print(e)
        echo("Removing Accoladez folder")
        subprocess.call(["sudo", "rm", "-rf", accoladez_base_path])
        echo("🚫 Accomate setup failed, please try again.")
        exit(code=1)
    except Exception as e:
        print(e)
        echo("Removing Accoladez folder")
        subprocess.call(["sudo", "rm", "-rf", accoladez_base_path])
        echo("🚫 Accomate setup failed, please try again.")
        exit(code=1)


@app.command()
def authenticate():
    pass


@app.command()
def init(store_name: str, template: str = "default"):
    """
    Initialize a new accoladez store project.

    @store_name: The name of the store.
    @template: The git address of the template repository.

    """

    GITHUB_PERSONAL_TOKEN = os.environ.get("GITHUB_PERSONAL_TOKEN")

    environment = input(
        "Client environment [dev, production] -> (default: production): ")
    service_version = input(
        "Compatible service version -> (default: latest): ")
    store_email = input("Store email: ")

    if template == "default":
        template = "accoladez-subscription-template"

    validate_email(store_email)

    if service_version == "" or service_version == "latest":
        latest_service_version = list(store_service_images.keys())[-1]
        service_version = latest_service_version

    environment = validate_enviorment(environment)

    echo(
        f"😉️ Choosen environment: {environment} and service version: {service_version}")

    echo("Calling the 🧙️ to do the 🪄️...")

    if GITHUB_PERSONAL_TOKEN is None:
        echo("💥 You must set the GITHUB_PERSONAL_TOKEN environment variable.")
        echo(
            "See https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line")
        raise typer.Exit(code=1)

    echo(f"😀️ Crafting the new store --({store_name})--")

    echo(f"Cloning template repository --({template})--")

    parsed_store_name = store_name.replace(" ", "_").lower()
    parsed_store_name = store_name.replace("-", "_").lower()

    repository_url = f"https://{GITHUB_PERSONAL_TOKEN}@github.com/Accoladez/{template}"

    repository_clone_path = f"{accoladez_base_store_path}/{parsed_store_name}"

    cloned = clone_repo(repository_url, repository_clone_path)

    if not cloned:
        echo("💥 Failed to clone repository")
        raise typer.Exit(code=1)

    # START---- TODO: Work on generating the domain and updating the DNS records. -----START

    doamin_prefix_rfc_1034 = parsed_store_name.replace("_", "-")

    auth_random = randomname.get_name()
    store_random = randomname.get_name()

    auth_service_domain = f"{auth_random}.{accoladez_base_domain}"
    store_service_domain = f"{store_random}.{accoladez_base_domain}"

    echo(f"Setting up store --({store_name})-- domains")

    auth_dns_response = add_dns_record(
        hosted_zone_id, "A", auth_service_domain, machine_ip_address)
    store_dns_response = add_dns_record(
        hosted_zone_id, "A", store_service_domain, machine_ip_address)

    if not auth_dns_response or not store_dns_response:
        echo("💥 Failed to add DNS record")
        raise typer.Exit(code=1)

    echo(f"🎉️ Store --({store_name})-- domains setup completed")

    # END---- TODO: Work on generating the domain and updating the DNS records. -----END

    key_response = write_all_the_keys(repository_clone_path)

    if key_response:
        echo(f"💾 All the keys are saved for --({store_name})--")
    else:
        typer.Abort("💥 Failed to write all the keys to the store.")

    echo(f"✏️ Editing docker-compose.yaml for --({store_name})--")

    docker_compose_file = f"{repository_clone_path}/docker-compose.yaml"

    compose_dict = read_yaml_file(docker_compose_file)

    # print(compose_dict)
    # exit()

    echo("💾 Updating docker-compose.yaml")

    # REDIS SETUP

    REDIS_PASSWORD = generate_random_password(22)

    compose_dict['services']['redis']['environment'][
        0] = f"REDIS_PASSWORD={REDIS_PASSWORD}"
    # compose_dict['services']['redis']['volumes'][0] = f"{parsed_store_name}-redis-data:/data"

    # MongoDB SETUP

    MONGODB_PASSWORD = generate_random_password(22)

    compose_dict['services']['mongodb']['environment'][
        0] = "MONGO_INITDB_ROOT_USERNAME=root"
    compose_dict['services']['mongodb']['environment'][
        1] = f"MONGO_INITDB_ROOT_PASSWORD={MONGODB_PASSWORD}"
    # compose_dict['services']['mongodb']['volumes'][
    #     0] = f"{parsed_store_name}-mongo-data:/data/db"

    # MySQL SETUP

    MYSQL_PASSWORD = generate_random_password(22)

    compose_dict['services']['mysql']['environment'][
        0] = f"MYSQL_ROOT_PASSWORD={MYSQL_PASSWORD}"
    # compose_dict['services']['mysql']['volumes'][
    #     0] = f"{parsed_store_name}-mysql-data:/var/lib/mysql"

    # Auth Service SETUP

    auth_service_port = find_open_port()

    compose_dict['services']['auth']['image'] = auth_service_images[service_version]
    compose_dict['services']['auth']['ports'][0] = f"{auth_service_port}:8000"
    compose_dict['services']['auth']['environment'][
        0] = f"ENVIRONMENT={environment}"
    compose_dict['services']['auth']['environment'][
        1] = f"DJANGO_SUPERUSER_USERNAME={parsed_store_name}"
    compose_dict['services']['auth']['environment'][
        2] = f"DJANGO_SUPERUSER_EMAIL={store_email}"

    # Store Service SETUP

    store_service_port = find_open_port()

    compose_dict['services']['store']['image'] = store_service_images[service_version]
    compose_dict['services']['store']['ports'][0] = f"{store_service_port}:8000"
    compose_dict['services']['store']['environment'][
        0] = f"ENVIRONMENT={environment}"
    compose_dict['services']['store']['environment'][
        1] = f"DJANGO_SUPERUSER_USERNAME={parsed_store_name}"
    compose_dict['services']['store']['environment'][
        2] = f"DJANGO_SUPERUSER_EMAIL={store_email}"

    # VOLUME SETUP

    # compose_dict['volumes'] = {}

    # compose_dict['volumes'][f"{parsed_store_name}-redis-data"] = None
    # compose_dict['volumes'][f"{parsed_store_name}-mongo-data"] = None
    # compose_dict['volumes'][f"{parsed_store_name}-mysql-data"] = None

    with open(f"{repository_clone_path}/accoladez.json", "w+", encoding="utf-8") as accoladez:
        json_data = {
            "store": {
                "name": store_name,
                "slug": parsed_store_name,
                "email": store_email,
                "template": template,
            },
            "environment": environment,
            "service_version": service_version,
            "urls": {
                "store_service": store_service_domain,
                "auth_service": auth_service_domain,
            },
            "secrets": {
                "redis_password": REDIS_PASSWORD,
                "mongodb_password": MONGODB_PASSWORD,
                "mysql_password": MYSQL_PASSWORD
            },
            "ports": {
                "store_service": store_service_port,
                "auth_service": auth_service_port
            },
        }
        json.dump(json_data, accoladez, indent=4)

    echo(f"💾 Writing docker-compose.yaml for --({store_name})--")
    write_yaml_file(docker_compose_file, compose_dict)
    echo("💾 Docker-compose.yaml is updated.")
    echo("😉️ Initialization is complete.")
    echo(
        f"🎉️ You can now run `accomate setup` in the project directory.")


@app.command()
def setup():
    """
    Setup the store.
    """

    execution_directory = os.getcwd()
    docker_compose_path = os.path.join(
        execution_directory, "docker-compose.yaml")
    auth_env_path = os.path.join(
        execution_directory, "docker", "envs", "auth.env")
    store_env_path = os.path.join(
        execution_directory, "docker", "envs", "store.env")
    project_config_path = os.path.join(execution_directory, "accoladez.json")
    directory_split = execution_directory.split("/")
    project_name = directory_split[-1]

    parsed_store_name = project_name.replace(" ", "_").lower()
    parsed_store_name_dir = project_name.replace(" ", "-").lower()
    parsed_store_name_dir = project_name.replace("_", "-").lower()

    # os.chdir(f"{accoladez_base_store_path}/{parsed_store_name}")

    try:
        with open(project_config_path, "r") as accoladez:
            json_data = json.load(accoladez)
            if not validate_project_config(json_data):
                echo("💥 The project config is not valid.")
                raise typer.Abort("💥 The project config is not valid.")
            else:
                accoladez_config = json_data

        if not accoladez_config:
            echo("💥 Failed to read accoladez.json")
            return
        else:
            echo("💾 Read accoladez.json")

            auth_service_domain = accoladez_config["urls"]["auth_service"]
            store_service_domain = accoladez_config["urls"]["store_service"]

            if verify_dns_record(hosted_zone_id, 'A', auth_service_domain, machine_ip_address):
                echo(
                    f"💾 Auth service domain {auth_service_domain} is verified.")
            else:
                echo(
                    f"💾 Auth service domain {auth_service_domain} is not verified.")
                raise typer.Abort(
                    f"💥 Auth service domain {auth_service_domain} is not verified.")
            if verify_dns_record(hosted_zone_id, 'A', store_service_domain, machine_ip_address):
                echo(
                    f"💾 Store service domain {store_service_domain} is verified.")
            else:
                echo(
                    f"💾 Store service domain {store_service_domain} is not verified.")
                raise typer.Abort(
                    f"💥 Store service domain {store_service_domain} is not verified.")

            ACCOLADEZ_APP_ID = generate_store_app_id(parsed_store_name)
            ACCOLADEZ_APP_SECRET = generate_store_app_key(parsed_store_name)

            AWS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
            AWS_SECRET = os.environ.get("AWS_SECRET_ACCESS_KEY")
            AMPQ_SERVER_URL = os.environ.get("AMPQ_SERVER_URL")
            AWS_REGION = "ap-south-1"
            AWS_BUCKET = parsed_store_name_dir

            if AWS_KEY is None or AWS_SECRET is None:
                echo("💥 AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY is not set.")
                raise typer.Abort()

            if AMPQ_SERVER_URL is None:
                echo("💥 AMPQ_SERVER_URL is not set.")
                raise typer.Abort()

            auth_env = dotenv.load_dotenv(auth_env_path, encoding="utf-8")

            bucket = s3.create_bucket(parsed_store_name_dir, AWS_REGION)

            if bucket is not None:
                echo("💾 S3 Bucket created successfully.")

                # AWS Config
                dotenv.set_key(auth_env_path,
                               "AWS_ACCESS_KEY_ID", AWS_KEY)
                dotenv.set_key(auth_env_path,
                               "AWS_SECRET_ACCESS_KEY", AWS_SECRET)
                dotenv.set_key(auth_env_path, "AWS_REGION", AWS_REGION)

                # Accoladez Config
                dotenv.set_key(auth_env_path,
                               "APP_ID", ACCOLADEZ_APP_ID)
                dotenv.set_key(auth_env_path,
                               "APP_KEY", ACCOLADEZ_APP_SECRET)

                # AMPQ Config
                dotenv.set_key(auth_env_path,
                               "AMPQ_SERVER", AMPQ_SERVER_URL)

                # DJANGO Config

                auth_service_url = accoladez_config['urls']['auth_service']

                ALLOWED_HOST = [
                    auth_service_url,
                    'localhost',
                ]

                ALLOWED_HOST = " ".join(ALLOWED_HOST)

                dotenv.set_key(auth_env_path,
                               "SECRET_KEY", generate_django_secret_key(55))
                dotenv.set_key(auth_env_path,
                               "ALLOWED_HOSTS", ALLOWED_HOST)

                # Remove Key Password

                if os.environ.get("GUEST_USER_PRIVATE_KEY_PASSPHRASE") is not None:
                    dotenv.unset_key(auth_env_path,
                                     "GUEST_USER_PRIVATE_KEY_PASSPHRASE")

                if os.environ.get("JWT_PRIVATE_KEY_PASSPHRASE") is not None:
                    dotenv.unset_key(auth_env_path,
                                     "JWT_PRIVATE_KEY_PASSPHRASE")

                # Auth Store Config

                STORE_SERVICE_URL = f"https://{accoladez_config['urls']['store_service']}"

                dotenv.set_key(auth_env_path,
                               "STORE_SERVICE", STORE_SERVICE_URL)

                # Auth MySQL Config

                MYSQL_HOST = "mysql"
                MYSQL_USER = "root"
                MYSQL_PASSWORD = accoladez_config['secrets']['mysql_password']

                dotenv.set_key(auth_env_path, "DB_HOST", MYSQL_HOST)
                dotenv.set_key(auth_env_path, "DB_USER", MYSQL_USER)
                dotenv.set_key(auth_env_path,
                               "DB_PASSWORD", MYSQL_PASSWORD)
                dotenv.set_key(auth_env_path, "DB_NAME",
                               "accoladez_auth_service")

                # Email Config

                EMAIL = f"{parsed_store_name}@store.accoladez.com"
                SENDER_NAME = project_name.capitalize().replace("_", " ")

                dotenv.set_key(auth_env_path,
                               "SENDER_MAIL", f"{SENDER_NAME} <{EMAIL}>")

                # Auth Frontend Config

                AUTH_FRONTEND_URL = input("Enter the Auth Frontend URL: ")
                dotenv.set_key(auth_env_path,
                               "BASE_URL", AUTH_FRONTEND_URL)

                # JWT Config

                dotenv.set_key(auth_env_path,
                               "JWT_AUDIENCE", "accoladez.com")
                dotenv.set_key(auth_env_path,
                               "JWT_ISSUER", "accoladez.com")

                # CORS Config

                STORE_FRONTEND_URL = input("Enter the Store Frontend URL: ")

                CORS_ALLOWED_ORIGINS = [
                    STORE_FRONTEND_URL,
                    AUTH_FRONTEND_URL,
                ]

                CSRF_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS

                CSRF_ALLOWED_ORIGINS.append(f"https://{auth_service_url}")

                CORS_ALLOWED_ORIGINS = " ".join(CORS_ALLOWED_ORIGINS)
                CSRF_ALLOWED_ORIGINS = " ".join(CSRF_ALLOWED_ORIGINS)

                dotenv.set_key(auth_env_path,
                               "COOKIE_HOST", ".accoladez.com")
                dotenv.set_key(auth_env_path,
                               "CORS_ALLOWED_ORIGINS", CORS_ALLOWED_ORIGINS)
                dotenv.set_key(auth_env_path,
                               "CSRF_TRUSTED_ORIGINS", CSRF_ALLOWED_ORIGINS)

                # Store ENV Config

                store_env = dotenv.load_dotenv(
                    store_env_path, encoding="utf-8")

                # CORS Config

                dotenv.set_key(store_env_path,
                               "COOKIE_HOST", ".accoladez.com")
                dotenv.set_key(store_env_path,
                               "CORS_ALLOWED_ORIGINS", CORS_ALLOWED_ORIGINS)
                dotenv.set_key(store_env_path,
                               "CSRF_TRUSTED_ORIGINS", CORS_ALLOWED_ORIGINS)

                # JWT Config

                dotenv.set_key(store_env_path,
                               "JWT_AUDIENCE", "accoladez.com")
                dotenv.set_key(store_env_path,
                               "JWT_ISSUER", "accoladez.com")

                # Store Auth Config
                dotenv.set_key(store_env_path,
                               "BASE_URL", AUTH_FRONTEND_URL)

                # AWS Config
                dotenv.set_key(store_env_path,
                               "AWS_ACCESS_KEY_ID", AWS_KEY)
                dotenv.set_key(store_env_path,
                               "AWS_SECRET_ACCESS_KEY", AWS_SECRET)
                dotenv.set_key(store_env_path,
                               "AWS_S3_REGION_NAME", AWS_REGION)
                dotenv.set_key(store_env_path,
                               "AWS_STORAGE_BUCKET_NAME", AWS_BUCKET)

                # AMPQ Config

                dotenv.set_key(store_env_path,
                               "AMPQ_SERVER", AMPQ_SERVER_URL)

                # DJANGO Config

                store_service_url = accoladez_config['urls']['store_service']

                ALLOWED_HOST = [
                    store_service_url,
                    'localhost',
                ]

                ALLOWED_HOST = " ".join(ALLOWED_HOST)

                dotenv.set_key(store_env_path,
                               "SECRET_KEY", generate_django_secret_key(55))
                dotenv.set_key(store_env_path,
                               "ALLOWED_HOSTS", ALLOWED_HOST)

                # Remove Key Password

                if os.environ.get("GUEST_USER_PRIVATE_KEY_PASSPHRASE") is not None:
                    dotenv.unset_key(store_env_path,
                                     "GUEST_USER_PRIVATE_KEY_PASSPHRASE")

                if os.environ.get("JWT_PRIVATE_KEY_PASSPHRASE") is not None:
                    dotenv.unset_key(store_env_path,
                                     "JWT_PRIVATE_KEY_PASSPHRASE")

                # MongoDB Config

                MONGODB_PASSWORD = accoladez_config['secrets']['mongodb_password']

                dotenv.set_key(store_env_path,
                               "DB_NAME", "store_service")
                dotenv.set_key(store_env_path,
                               "DB_CLIENT_HOST", "mongodb")
                dotenv.set_key(store_env_path,
                               "DB_CLIENT_USERNAME", "root")
                dotenv.set_key(store_env_path,
                               "DB_CLIENT_PASSWORD", MONGODB_PASSWORD)

                # Redis Config

                REDIS_PASSWORD = accoladez_config['secrets']['redis_password']

                dotenv.set_key(store_env_path,
                               "DB_CACHES_LOCATION", f"redis://redis:6379")
                dotenv.set_key(store_env_path, "DB_CACHES_DB", "1")
                dotenv.set_key(store_env_path,
                               "DB_CACHES_PASSWORD", REDIS_PASSWORD)
                dotenv.set_key(store_env_path,
                               "DB_CACHES_KEY_PREFIX", parsed_store_name)

                echo("😉️ Setup is done.")
                echo(
                    f"🎉️ You can now run `accomate up` in the project directory.")

            else:
                echo("💥 Bucket already exists.")
                raise typer.Abort()

    except FileNotFoundError as e:
        echo("💥 The store is not initialized.")
        raise typer.Abort("💥 The store is not initialized.")
    except Exception as e:
        echo(f"💥 {e}")
        raise typer.Abort()


@app.command()
def up(restart: bool = False):
    """
    Up the store
    """
    # compose up the docker-compose.yaml
    try:
        execution_directory = os.getcwd()
        project_config_path = os.path.join(
            execution_directory, "accoladez.json")
        directory_split = execution_directory.split("/")
        project_name = directory_split[-1]
        dns_test_attempts = 0

        parsed_dir = project_name.replace(" ", "_")

        try:
            with open(project_config_path, "r") as config:
                project_config = json.load(config)
                if not validate_project_config(project_config):
                    echo("💥 The project config is not valid.")
                    raise typer.Abort("💥 The project config is not valid.")

        except FileNotFoundError as e:
            echo("💥 The store is not initialized.")
            raise typer.Abort("💥 The store is not initialized.")

        # Loading important configs
        auth_service_domain = project_config['urls']['auth_service']
        store_service_domain = project_config['urls']['store_service']
        auth_service_proxy_pass = f"http://localhost:{project_config['ports']['auth_service']}"
        store_service_proxy_pass = f"http://localhost:{project_config['ports']['store_service']}"
        auth_service_static_files_path = f"{execution_directory}/static/auth"
        store_service_static_files_path = f"{execution_directory}/static/store"
        store_email = project_config['store']['email']

        echo("🚀 Uping the store...")
        compose_up(execution_directory)
        total_service_start_wait_time = 20  # TODO: Please change it to 20
        echo("🚀 Waiting for services to start...")
        with typer.progressbar(range(total_service_start_wait_time)) as progress:
            for i in progress:
                time.sleep(1)
        echo("Services are up.")
        echo("✅ Verifying DNS...")

        domains = [auth_service_domain, store_service_domain]

        dns_check(hosted_zone_id, domains)

        service_containers = get_containers_on_same_network(
            f"{parsed_dir}_default")
        services_by_tags = assign_service_type_tag(
            service_containers, parsed_dir)
        auth_container_id = services_by_tags['auth'].get('id')

        if restart:
            auth_restart_response = restart_containers(auth_container_id)
            if auth_restart_response:
                echo("\n🚀 Auth service restarted.")
            else:
                echo("💥 Auth service failed to restart.")

        echo("🚀 Starting Nginx setup")

        try:
            with open(f"{absolute_package_path}/conf/nginx/site.conf", "r") as site_template:
                template = site_template.read()

                auth_service_nginx_conf = template
                store_service_nginx_conf = template

                os.makedirs(base_nginx_path, exist_ok=True)

                # Mofifing the template for auth_service
                auth_service_nginx_conf = auth_service_nginx_conf.replace(
                    "#domain#", auth_service_domain)
                auth_service_nginx_conf = auth_service_nginx_conf.replace(
                    "#static_files_path#", auth_service_static_files_path)
                auth_service_nginx_conf = auth_service_nginx_conf.replace(
                    "#proxy_pass_uri#", auth_service_proxy_pass)

                echo("Writing auth_service nginx conf...")
                with open(f"{base_nginx_path}/{auth_service_domain}.conf", "w+") as f:
                    f.write(auth_service_nginx_conf)

                # Mofifing the template for store_service
                store_service_nginx_conf = store_service_nginx_conf.replace(
                    "#domain#", store_service_domain)
                store_service_nginx_conf = store_service_nginx_conf.replace(
                    "#static_files_path#", store_service_static_files_path)
                store_service_nginx_conf = store_service_nginx_conf.replace(
                    "#proxy_pass_uri#", store_service_proxy_pass)

                echo("Writing store_service nginx conf...")
                with open(f"{base_nginx_path}/{store_service_domain}.conf", "w+") as f:
                    f.write(store_service_nginx_conf)

                echo("✅ Verifying Configuration...")

                verify_nginx_conf()

                echo("🔒 Let's Encrypt Setup")

                add_lets_encrypt_certificate(auth_service_domain, store_email)
                add_lets_encrypt_certificate(store_service_domain, store_email)

                echo("🔒 Let's Encrypt Setup Done")

                echo("🚀 Re-starting Nginx...")

                restart_nginx()

                echo("✅ Nginx is up.")

        except FileNotFoundError as e:
            print(e)
            echo("💥 Not able to find template site.conf.")
            raise typer.Abort()
        except Exception as e:
            print(e)
            echo("💥 Not able to find template site.conf.")
            raise typer.Abort()
    except Exception as e:
        echo(f"💥 {e}")
        raise typer.Abort()


@app.command()
def finalize():
    try:

        execution_directory = os.getcwd()
        project_config_path = os.path.join(
            execution_directory, "accoladez.json")
        directory_split = execution_directory.split("/")
        project_name = directory_split[-1]

        parsed_dir = project_name.replace(" ", "_")
        parsed_dir_with_hyphen = parsed_dir.replace("_", "-")

        try:
            with open(project_config_path, "r") as config:
                project_config = json.load(config)
                if not validate_project_config(project_config):
                    echo("💥 The project config is not valid.")
                    raise typer.Abort("💥 The project config is not valid.")

        except FileNotFoundError as e:
            echo("💥 The store is not initialized.")
            raise typer.Abort("💥 The store is not initialized.")

        echo("🚀 Finalizing...")
        subprocess.call(["pwd"])
        subprocess.call(["sudo", "chmod", "-R", "777", "static/"])
        subprocess.call(["sudo", "chown", "-R", f"{USER}:{USER}", "static/"])

        echo("🚀 Finalizing Done")
    except Exception as e:
        echo(f"💥 {e}")
        raise typer.Abort()


@app.command()
def down():
    """
    Down the store
    """
    try:

        execution_directory = os.getcwd()
        project_config_path = os.path.join(
            execution_directory, "accoladez.json")
        directory_split = execution_directory.split("/")
        project_name = directory_split[-1]

        parsed_dir = project_name.replace(" ", "_")
        parsed_dir_with_hyphen = parsed_dir.replace("_", "-")

        try:
            with open(project_config_path, "r") as config:
                project_config = json.load(config)
                if not validate_project_config(project_config):
                    echo("💥 The project config is not valid.")
                    raise typer.Abort("💥 The project config is not valid.")

        except FileNotFoundError as e:
            echo("💥 The store is not initialized.")
            raise typer.Abort("💥 The store is not initialized.")

        echo("🚀 Downing the store...")
        compose_down(execution_directory)

        echo("🚀 Closed")
    except Exception as e:
        echo(f"💥 {e}")
        raise typer.Abort()


@app.command()
def test():
    total = 0
    users = ["Camila", "Rick", "Morty"]

    with typer.progressbar(users) as progress:
        for user in progress:
            typer.echo(user)
