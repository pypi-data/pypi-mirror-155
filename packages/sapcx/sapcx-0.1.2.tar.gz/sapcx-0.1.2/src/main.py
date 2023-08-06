import sys

import src.api as api
import src.cli as cli
import src.profile as profile
from src.console import flexiblesearch
from src.console import scripting
from src.console import impex


def main():
    if len(sys.argv) <= 1:
        cli.cli.print_help()
        exit(1)

    args = cli.cli.parse_args()

    if args.subcli and args.subcli == 'configure':
        user_profile = profile.get_profile_from_user()
        user_profile.save()
        exit(0)

    user_profile = profile.Profile(args.profile)
    user_profile.load()

    api_client = api.SAPAPI(
        username=user_profile.username,
        password=user_profile.password,
        hacurl=user_profile.get_hac_url()
    )
    api_client.login()

    impex_console = impex.ImpexEngine(api_client)
    scripting_console = scripting.Scripting(api_client)
    flexiblesearch_console = flexiblesearch.FlexibleSearch(api_client)

    if args.import_impex:
        file = args.import_impex
        impex_script = impex.Impex(file, is_file=True)
        result = impex_console.impex_import(impex_script)
        if result.is_ok():
            print(f"Impex {file} executed successfully")
            exit(0)
        else:
            print(result.get_errors())
            exit(2)

    if args.execute_groovy:
        file = args.execute_groovy
        script = scripting.Script(file, is_file=True)
        result = scripting_console.execute(script)
        if result.is_ok():
            print(result.output)
            exit(0)
        else:
            print(result.get_errors())
            exit(2)

    if args.query:
        query = args.query
        result = flexiblesearch_console.execute(query)
        if result.is_ok():
            print(result.get_result())
            exit(0)
        else:
            print(result.get_errors())
            exit(2)


if __name__ == '__main__':
    main()
