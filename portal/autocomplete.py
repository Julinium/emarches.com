# from datetime import date, datetime, timedelta
# from django.shortcuts import render
# from django.db.models import Q

# from .models import Consultation

# SPLIT_TERMS = False
# SUGGESTIONS_LOADED = 10


# def locations(request):
#     query = request.GET.get("l", "").strip()
#     locations = []

#     if SPLIT_TERMS:
#         if query:
#             search_terms = query.split()
#             q_filter = Q()
#             for term in search_terms:
#                 if len(term) > 2 :
#                     q_filter |= Q(lieu_execution__unaccent__icontains=term)  # OR condition for each term

#             locations = Consultation.objects.filter(date_limite_depot__gte = datetime.now() - timedelta(hours=1)).filter(q_filter).order_by('lieu_execution').values_list("lieu_execution", flat=True).distinct()[:SUGGESTIONS_LOADED]
#     else:
#         locations = Consultation.objects.filter(date_limite_depot__gte = datetime.now() - timedelta(hours=1)).filter(lieu_execution__unaccent__icontains=query).values_list("lieu_execution", flat=True).distinct()[:SUGGESTIONS_LOADED]

#     return render(request, "portal/suggestions/locations.html", {"locations": locations})



                            # <!-- <div class="col-12">
                            #     <div id="groupLocation" class="input-group mt-2">
                            #         <span class="input-group-text small text-muted" id="locationSpan">{% translate 'Exec. Location' %}</span>
                            #         <input
                            #             type="text" 
                            #             name="l" 
                            #             class="form-control dropdown-toggle" 
                            #             value="{% if qd.l %}{{ qd.l }}{% endif %}" 
                            #             class="form-control" id="locationInput" 
                            #             aria-describedby="locationSpan" 
                            #             hx-get="{% url 'locations' %}" 
                            #             hx-trigger="keyup changed delay:200ms" 
                            #             hx-target="#location-suggestions" 
                            #             data-bs-toggle="dropdown" 
                            #             aria-expanded="false" 
                            #             hx-include="#locationInput">
                            #         <ul id="location-suggestions" class="dropdown-menu" style="max-height: auto; overflow-y: auto;"></ul>
                            #         <style>
                            #             .htmx-indicator {
                            #                 display: none;
                            #             }
                            #             .htmx-request .htmx-indicator {
                            #                 display: inline;
                            #             }
                            #         </style>
                            #     </div>
                            # </div> -->