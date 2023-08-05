import requests
import json
import os
import time
import re
import multiprocessing
import threading

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://myretailcorp-poc.arecabay.net',
    'Authorization': 'Bearer null',
    'X-AB-Trace-ID': 'null-93adb9098c225bbbf754a4ceca135d285477c0cbc33e957f8faf9e1c9e95a18d',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
    'Content-Type': 'application/json',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://myretailcorp-poc.arecabay.net/customer/login',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

API_SPEC = {
    "basePath": "/",
    "info": {},
    "paths": {},
    "schemes": [
        "http"
    ],
    "swagger": "2.0"
}


class CommunityEdition(object):
    def __init__(self, host_url, username, password):
        self.host_url = host_url
        self.username = username
        self.password = password
        self.tenantid = "1000"
        self.total_unique_apis = 0
        self.total_api_events = 0
        self.total_apis_inspec_captured = 0
        self.api_sec_details = {"auth": 0, "noauth": 0}
        try:
            self.get_access_token()
        except:
            print("Check your CE info provided!")
            raise SystemExit

    def get_access_token(self):
        global headers
        data = {"email": self.username, "password": self.password}
        response = requests.post(self.host_url + "/ce-api/auth/tenant/login", headers=headers, data=json.dumps(data))
        if response.status_code in [500]:
            print("Issue with the CE setup, Please check! status code: " + str(response.status_code))
            raise SystemExit
        elif response.status_code in [401, 403]:
            print("Please check your credentials!")
            raise SystemExit
        try:
            headers["Authorization"] = "Bearer " + str(response.json()["auth_token"])
        except KeyError:
            print("\nPlease check your Community Edition (CE) credentials!\n")
            raise SystemExit
        print("\nAuthentication to Community Edition Successful!\n")
        self.tenantid = response.json()["tenant_user"]["tenant_unique_id"]
        return response.json()["auth_token"]

    def _get_all_policies(self):
        params = (
            ('page', '1'),
            ('size', '20'),
        )

        response = requests.get(self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/policies/of/api_recorder',
                                headers=headers, params=params, verify=False)
        policies = {}
        for each in response.json()["data"]:
            policies[each["attributes"]["name"]] = each["id"]
        return policies

    def get_policyid_from_name(self, policy):
        try:
            policies_for_tenant = self._get_all_policies()
        except:
            return None
        return policies_for_tenant[policy]

    def get_api_details_for_recording(self, policy):
        global API_SPEC
        data = {"filter_attributes": {"is_api": True}}
        api_details = {}
        try:
            policyid = self.get_policyid_from_name(policy)
        except KeyError:
            print("Please check the recording name provided!")
            raise SystemExit
        if policy:
            response = requests.post(
                self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/policies/of/api_recorder/' + str(
                    policyid) + '/assoc',
                headers=headers, data=json.dumps(data), verify=False)

            for each in response.json()["data"]["data"]["attributes"]["data"]:
                self.total_unique_apis += 1
                API_SPEC["paths"][each["grouped_api"]] = {str(each["method"]).lower(): {"parameters": []}}
                if each["body_params"]:
                    for _ in each["body_params"]:
                        API_SPEC["paths"][each["grouped_api"]][str(each["method"]).lower()]["parameters"].append({
                            "in": "body",
                            "name": _["parameter_name"],
                            "required": str(_["optional"]),
                            "type": _["parameter_datatype"]
                        })
            self.total_api_events = self.total_unique_apis
            return API_SPEC
        else:
            print("probably not a valid Policy/recording name provided")

    def _multiple_requests(self, url, headers, data, page):
        print("::::" + str(page))
        data["page"] = page
        print(data)
        # print(str(self.page)+"::::")
        attempt = 0
        # while attempt < 5:
        #     try:
        #         resp = requests.post(url,headers=headers,data=json.dumps(data), verify=False)
        #     except:
        #         pass
        #     attempt += 1
        #     print(resp.status_code)
        #     if resp.status_code == 200:
        #         break
        #     print("retrying..."+str(data))
        #     time.sleep(5)
        resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
        if resp.status_code == 200:
            return json.dumps(resp.json())
        else:
            return json.dumps({"data": []})

    def _get_params_for_events(self, api_name, start_time, end_time):
        import time
        start = time.time()
        data = {"from_time": start_time,
                "to_time": end_time,
                "page": 1, "size": int(os.environ.get("MAX_CVEVENTS_TO_PROCESS", 10000)),
                "search": {"http_host": None,
                           "api": api_name,
                           "client_ip": None,
                           "destination_ip": None,
                           "destination_port": None,
                           "http_method": None,
                           "http_rsp_status_code": None},
                "filter_attributes": {"is_api": True}}

        # resp = requests.post(self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/events/search',
        #                      headers=headers, data=json.dumps(data), verify=False)
        # num_of_events = resp.json()["meta"]["total"]
        # print("*****"+str(num_of_events))
        # pool_size = 10#int(num_of_events/2000)
        # data["size"] = 1000
        # from multiprocessing.pool import ThreadPool
        # pool = ThreadPool(pool_size)
        # workers = []
        # print("pool size:"+str(pool_size))
        # for _ in range(1,pool_size+1):
        #     workers.append(pool.apply_async(self._multiple_requests, args=(
        #         self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/events/search', headers, data, _)))
        # # results = pool.map(self._multiple_requests,[])
        # pool.close()
        # pool.join()
        # results = []
        # for worker in workers:
        #     print("\n\n"+str(worker))
        #     result = worker.get()
        #     # print(result)
        #     results.extend(json.loads(result)["data"])
        # print("ppppppp"+str(len(results)))
        # # results = [r.get() for r in results]
        # # results =
        # # response = requests.post(self.host_url + '/ce-api/v1/tenants/'+self.tenantid+'/events/search', headers=headers,
        # #                         data=json.dumps(data), verify=False, timeout=120)
        # # print((time.time()-start)/60)
        all_events_captured = {}
        # # print(response.status_code)
        # # print(response.text)
        attempts = 1
        # start = time.time()
        while attempts <= 3:
            response = requests.post(self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/events/search',
                                     headers=headers, data=json.dumps(data), verify=False, timeout=120)
            attempts += 1
            if response.status_code == 200:
                break
        # print((time.time()-start))
        for event in response.json()["data"]:
            # events = set()
            # for event in results:
            # if event["id"] in events:
            #    print("already present......")
            # events.add(event["id"])
            all_events_captured[event["id"]] = {
                "params": event["attributes"]["event_json"].get("http-req-body-params", []),
                "response_code": str(event["attributes"]["event_json"].get("http-rsp-Status", "")).split(" ")[0]
            }
            query_params = []
            if "http-req-query-params" in event["attributes"]["event_json"]:
                all_events_captured[event["id"]]["params"] += event["attributes"]["event_json"]["http-req-query-params"]
            if event["attributes"]["event_json"].get("http-req-header-Authorization"):
                all_events_captured[event["id"]].update({"is_api_secured": [True]})
            else:
                all_events_captured[event["id"]].update({"is_api_secured": [False]})
        # print("all events:"+str(len(events)))
        return all_events_captured

    def get_all_raw_events(self, apis_to_check=[], **kwargs):
        if os.environ.get("apishark_event_days"):
            time_period = int(os.environ["apishark_event_days"])
        else:
            time_period = 21  # days
        max_events = os.environ.get("MAX_CVEVENTS_TO_PROCESS", 5000)
        time_period = 60 * 60 * 24 * int(time_period)
        if apis_to_check:
            all_data = []
            all_apis = list(apis_to_check.keys())
            for api in apis_to_check:
                actual_api = api
                if "{" in api:
                    api = api.split("{")[0]
                similar_apis = []
                for each in all_apis:
                    if each.find(api) > 0:
                        similar_apis.append(each)
                data = {"is_api": True, "end_time": int(time.time()),
                        "start_time": int(time.time()) - time_period,
                        "api": str(api).lower(), "size": max_events}
                # if similar_apis:
                #     data["api"]

                data.update(kwargs)
                response = requests.post(self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/events/search',
                                         headers=headers,
                                         data=json.dumps(data), verify=False)
                # print("Events collected and analysed for "+str(actual_api)+" : "+str(len(response.json()["data"])))
                old_len = len(all_data)
                for _ in response.json()["data"]:
                    api = '(.*)'+re.sub('{.*?}', '(.*)', actual_api, flags=re.DOTALL)
                    _["api_queried"] = actual_api
                    try:
                        re.match(api, _["attributes"]["api"]).group(1)
                    except IndexError:
                        pass
                    except AttributeError:
                        pass
                    all_data.append(_)
                print("Events collected and analysed for " + str(actual_api) + " : " + str(len(all_data) - old_len))
            #                all_data += response.json()["data"]

            return all_data
        else:
            data = {"is_api": True, "end_time": int(time.time()),
                    "start_time": int(time.time()) - time_period,
                    "size": 5000}
            data.update(kwargs)
            response = requests.post(self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/events/search',
                                     headers=headers,
                                     data=json.dumps(data), verify=False)
            return response.json()["data"]

    def _get_api_specific_details(self, apiname, start_time, end_time):
        global headers
        self.total_apis_inspec_captured += 1
        data = {"is_api": True, "from_time": start_time, "to_time": end_time}
        if not self.total_api_events:
            response = requests.post(self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/events/search',
                                     headers=headers,
                                     data=json.dumps(data), verify=False)
            self.total_api_events = response.json()["meta"]["total"]
            print("           Total events captured for all APIs in CV Controller: " + str(self.total_api_events))
        all_events_captured = self._get_params_for_events(apiname, start_time, end_time)
        print("           Total events captured for " + str(apiname) + ": " + str(
            len(all_events_captured)))
        api_auth = []
        resp_code = []
        params_found_for_api = []

        for k, v in all_events_captured.items():
            params_found_for_api.extend(v["params"])
            api_auth.extend(v["is_api_secured"])
            resp_code.append(v["response_code"])

        if all(api_auth):
            self.api_sec_details["auth"] += 1
        else:
            self.api_sec_details["auth"] += 1
        return list(set(params_found_for_api)), api_auth, list(set(resp_code)), len(all_events_captured)

    # def _get_api_specific_details(self, groupid, start_time, end_time):
    #     global headers
    #     data = {"group_id": groupid, "start_time": start_time, "end_time": end_time, "page": 1, "size": 1}
    #
    #     response = requests.post(self.host_url + '/ce-api/v1/tenants/1000/summary/pg/discovery/api_details',
    #                              headers=headers, data=json.dumps(data), verify=False)
    #     total_count = response.json()["data"]["attributes"]["total"]
    #     data["size"] = total_count
    #     self.total_api_events += total_count
    #     response = requests.post(self.host_url + '/ce-api/v1/tenants/1000/summary/pg/discovery/api_details',
    #                              headers=headers, data=json.dumps(data), verify=False)
    #     params_found_for_api = []
    #     api_name = response.json()["data"]["attributes"]["data"][0]["api"]
    #
    #     all_events_captured = self._get_params_for_events(api_name, start_time, end_time)
    #     print("           Total events captured for " + str(api_name) + ": " + str(
    #         len(all_events_captured)))
    #     api_auth = []
    #     resp_code = []
    #     for k, v in all_events_captured.items():
    #         params_found_for_api.extend(v["params"])
    #         api_auth.extend(v["is_api_secured"])
    #         resp_code.append(v["response_code"])
    #
    #     if all(api_auth):
    #         self.api_sec_details["auth"] += 1
    #     else:
    #         self.api_sec_details["auth"] += 1
    #     return list(set(params_found_for_api)), api_auth, list(set(resp_code))

    def get_all_events(self, time_period):
        import time
        data = {"filter_attributes": {"type": "all"}, "end_time": int(time.time()),
                "start_time": int(time.time()) - time_period,
                "page": 1, "size": 200}

        response = requests.post(
            self.host_url + '/ce-api/v1/tenants/' + self.tenantid + '/summary/pg/discovery/api_list',
            headers=headers, data=json.dumps(data), verify=False)

        if response.status_code != 200:
            response = requests.post(self.host_url + '/ce-api/v1/tenants/20000/summary/pg/discovery/api_list',
                                     headers=headers, data=json.dumps(data), verify=False)
            if response.status_code != 200:
                print("API details not returned!")
                raise SystemExit

        all_api = response.json()["data"]
        if all_api:
            all_api = all_api["attributes"]["data"]
        return all_api

    def get_all_api_details(self, apis_to_lookup=[], time_period=3):
        # time_period mentioned above is 3 weeks
        import time
        if os.environ.get("apishark_event_weeks"):
            time_period = int(os.environ["apishark_event_weeks"])
        time_period = 60 * 60 * 24 * 7 * int(time_period)
        data = {"filter_attributes": {"type": "all"}, "end_time": int(time.time()),
                "start_time": int(time.time()) - time_period,
                "page": 1, "size": 200}
        #
        # response = requests.post(self.host_url + '/ce-api/v1/tenants/'+self.tenantid+'/summary/pg/discovery/api_list',
        #                          headers=headers, data=json.dumps(data), verify=False)
        #
        # if response.status_code != 200:
        #     response = requests.post(self.host_url + '/ce-api/v1/tenants/20000/summary/pg/discovery/api_list',
        #                              headers=headers, data=json.dumps(data), verify=False)
        #     if response.status_code != 200:
        #         print("API details not returned!")
        #         raise SystemExit
        #     #self.tenantid = "20000"
        #
        # all_api = response.json()["data"]
        # if all_api:
        #     all_api = all_api["attributes"]["data"]
        all_api = self.get_all_events(time_period)
        # print("Total API(s) captured in APIShark: " + str(len(all_api)))
        self.total_unique_apis = len(all_api)
        api_info = {}

        for apigroup in all_api:
            api_to_query = apigroup["api"]
            # if api_to_query == "/v1/*":
            #     api_to_query = "/v1/feedItems/carousels/moreLikeThis"
            #     apigroup["api"] = "/v1/feedItems/carousels/moreLikeThis"
            if apis_to_lookup:
                if apigroup["api"] not in apis_to_lookup:
                    iflag = False
                    #print("checking for ", apigroup["api"])
                    for each in apis_to_lookup:
                        #print("......", each)
                        actual_api = each
                        each = each.split("{")[0]
                        pos = each.count("/")+1
                        temp = apigroup["api"].split("/")
                        res = "/".join(temp[:pos])
                        #print(apis_to_lookup)
                        # print(res)
                        # print(each)
                        #print("\n\n",res, each,":::::::?????")
                        if res == each:
                            #print("matched....", apigroup["api"], actual_api)
                            api_to_query = res
                            iflag = True
                            break
                    if not iflag:
                        continue
            #print("\n\n","To query for api: ", api_to_query)
            params_found = []
            params, api_auth, resp_code, events_count = self._get_api_specific_details(api_to_query,
                                                                                       data["start_time"],
                                                                                       data["end_time"])
            for _ in params:
                params_found.append({"in": "body",
                                     "name": _,
                                     "required": "True",
                                     "type": "?"
                                     })
            # api_info[apigroup["api"]] = {"parameters":params_found}
            responses_captured = {}
            for _ in resp_code:
                if _:
                    responses_captured[str(_)] = {"description": ""}

            if apigroup["api"] not in API_SPEC["paths"]:
                API_SPEC["paths"][apigroup["api"]] = {}
            if str(apigroup["method"]).lower() not in API_SPEC["paths"][apigroup["api"]]:
                API_SPEC["paths"][apigroup["api"]][str(apigroup["method"]).lower()] = {
                    "parameters": params_found,
                    "responses": responses_captured,
                    "events_count": events_count,
                    "security": [{
                        "type": "oauth2",
                        "authorizationUrl": "",
                        "flow": "implicit",
                        "scopes": {}
                    }]
                }

        return API_SPEC


if __name__ == "__main__":
    ce = CommunityEdition("http://52.203.107.217:4200", "sandeepy@cloudvector.com", "Abcd1234$!")
    # print(ce.get_api_details_for_recording("Gb_test_30_Jan"))
    x = ce.get_all_raw_events(apis_to_check=[])
    print(x)
    print(len(x))
