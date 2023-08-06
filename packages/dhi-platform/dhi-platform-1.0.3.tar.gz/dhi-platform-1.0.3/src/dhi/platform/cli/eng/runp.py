#!/usr/bin/env python
import asyncio, platform
from dhi.platform.args import ClientArgs
from dhi.platform.config import ClientConfig
from dhi.platform.eventinghelper import ExecutionSession
from dhi.platform.generated.enginegen import EngineGenClientV2
from dhi.platform.generated.metadatagen import MetadataGenClientV2, MetadataGenClientV3
from dhi.platform.fmt import Format

def __initParser(parser):
    parser.add_argument("-f", "--inputfile", default=ClientArgs.GetDefault("DHIINPUT"), help="Input file path")
    parser.add_argument("-w", "--wait", default=False, help="Wait to finish", action="store_true")
    parser.add_argument("-l", "--showlog", default=False, help="Show log", action="store_true")

async def main():
    args = ClientArgs.ParseForProject(description="Run engine", init=__initParser, defaultformat="yaml")
    ClientConfig.UpdateProjectFromConfiguration(args)
    clientv2 = EngineGenClientV2(**vars(args))

    metadataclientv2 = MetadataGenClientV2(**vars(args))
    metadataclientv3 = MetadataGenClientV3(**vars(args))
    executionsession = ExecutionSession(args.showlog, metadataclientv2, metadataclientv3, args.verbose)
    async with executionsession.subscribe(args.projectid, ["/dhi/platform/engineexecution"], 200, None):
        try:
            await executionsession.wait_pubsubconnected()

            input = ClientArgs.LoadJson(args.inputfile)
            if args.showlog:
                modelitems = input.get("models")
                if modelitems:
                    for i in modelitems:
                        if i.get("engine"):
                            tmp = i.get("reportLogUpdatesLines")
                            if not tmp or tmp == 0:
                                i["reportLogUpdatesLines"] = 300
            response = clientv2.RunExecutionWithPlatformData(args.projectid, input)

            executionsession.set_resourceid(response.Body.get("executionId"))

            tablefields = ["executionId", "outputLocation"]
            Format.FormatResponse(response, lambda r: r.Body, args.format, None, tablefields)

            if args.wait:
                await executionsession.wait_finished()
        finally:
            await executionsession.wait(0)

if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
