from diagrams import Diagram, Edge, Cluster  # type: ignore[import]

from diagrams.generic.network import Router, Switch, Firewall
from diagrams.generic.os import Windows, IOS, LinuxGeneral
from diagrams.generic.storage import Storage
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Internet
from diagrams.onprem.client import User
from diagrams.programming.language import Python
from diagrams.generic.place import Datacenter
from diagrams.custom import Custom

with Diagram(
    name="BoM Scraper",
    show=False,
    filename="arch",
    outformat="png",
    graph_attr={"packMode": "graph"},
):
    with Cluster(""):
        bom = Custom("", "./resources/bom_logo.jpg")
        bom_json = Server("Datalake (JSON)")
        bom_website = Internet("Website")

    with Cluster("hh.home"):
        with Cluster(""):
            # Docker('')
            python = Python("BOM-Scraper")
            cron = Custom("Scheduler", "./resources/cron.png")
            python << cron

        with Cluster("Monitoring"):
            healthchecks = Custom(
                "Healthchecks", "./resources/healthchecks.io_logo.jpg"
            )
            signal = Custom("Signal", "./resources/signal_logo.png")
            healthchecks >> signal

        with Cluster("Storage"):
            storage = Storage("filesystem")

    [bom_json, bom_website] >> python >> [healthchecks, storage]
