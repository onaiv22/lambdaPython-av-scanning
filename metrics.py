import os

import datadog
from common import *  # noqa


def send(env, bucket, key, status):
    if "DATADOG_API_KEY" in os.environ:
        datadog.initialize()  # by default uses DATADOG_API_KEY

        result_metric_name = "unknown"

        metric_tags = ["env:%s" % env, "bucket:%s" % bucket, "object:%s" % key]

        if status == AV_STATUS_CLEAN:
            result_metric_name = "clean"
        elif status == AV_STATUS_INFECTED:
            result_metric_name = "infected"
            datadog.api.Event.create(
                title="Infected S3 Object Found",
                text="Virus found in s3://%s/%s." % (bucket, key),
                tags=metric_tags,
            )

        scanned_metric = {
            "metric": "s3_antivirus.scanned",
            "type": "counter",
            "points": 1,
            "tags": metric_tags,
        }
        result_metric = {
            "metric": "s3_antivirus.%s" % result_metric_name,
            "type": "counter",
            "points": 1,
            "tags": metric_tags,
        }
        print("Sending metrics to Datadog.")
        datadog.api.Metric.send([scanned_metric, result_metric])
