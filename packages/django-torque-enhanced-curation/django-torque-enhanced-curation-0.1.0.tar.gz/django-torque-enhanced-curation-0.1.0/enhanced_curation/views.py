from django.http import HttpResponse, JsonResponse, FileResponse
from torque import models
import random

def ranked_proposals(request):
    group = request.GET["group"]
    global_wiki_key = request.GET["wiki_key"]
    global_collection_name = request.GET["collection_name"]
    wiki_keys = request.GET["wiki_keys"].split(",")
    collection_names = request.GET["collection_names"].split(",")
    global_config = models.WikiConfig.objects.get(
        collection__name=global_collection_name,
        wiki__wiki_key=global_wiki_key,
        group=group,
    )
    configs = models.WikiConfig.objects.filter(
        collection__name__in=collection_names, wiki__wiki_key__in=wiki_keys, group=group
    ).all()

    proposals = random.sample(list(models.Document.objects.filter(collection__name__in=collection_names)), 10)

    resp = []
    for proposal in proposals:
        for config in configs:
            if config.collection == proposal.collection:
                resp.append(proposal.to_dict(config))

    return JsonResponse({"result": resp})
