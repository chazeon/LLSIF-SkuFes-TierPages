import os.path
import urllib.parse
import json
import requests

MINIMUM_EVENT_ID = 97
SKUFES_API_DOMAIN = 'https://api.skufes.moe'
SKUFES_API_EVENT_ENDPOINT= '/db/event/'
SKUFES_API_UNIT_ENDPOINT= '/db/unit/'
SKUFES_CARD_IMAGE_DOMAIN = 'https://skufes-card-images-intl.zeoncdn.cn'
SKUFES_CARD_IMAGE_ENDPOINT = '/framed/icon/'
ICON_TYPE_EVENT_POINT_COUNT_IDOLIZED = 1
ICON_TYPE_EVENT_POINT_RANKING_IDOLIZED = 2
ICON_TYPE_EVENT_POINT_COUNT_NORMAL = 3
ICON_TYPE_EVENT_POINT_RANKING_NORMAL = 4
ICON_TYPES = [
    ICON_TYPE_EVENT_POINT_COUNT_IDOLIZED,
    ICON_TYPE_EVENT_POINT_RANKING_IDOLIZED,
    ICON_TYPE_EVENT_POINT_COUNT_NORMAL,
    ICON_TYPE_EVENT_POINT_RANKING_NORMAL
]

class EventRewardUnitIconGetter:
    def __init__(self):
        self.units_summary = self.getUnitsSummary()
        self.events_summary = self.getEventsSummary()
    def getUnitsSummary(self) -> list:
        units_summary_url = urllib.parse.urljoin(SKUFES_API_DOMAIN, SKUFES_API_UNIT_ENDPOINT)
        response = requests.get(units_summary_url)
        if response.status_code != 200:
            pass
        units_summary = response.json()
        return units_summary
    def getEventsSummary(self) -> list:
        events_summary_url = urllib.parse.urljoin(SKUFES_API_DOMAIN, SKUFES_API_EVENT_ENDPOINT)
        response = requests.get(events_summary_url)
        if response.status_code != 200:
            pass
        events_summary = response.json()
        return events_summary
    def getUnitIcon(self, unit_id: int, event_id: int, icon_type: int):
        unit = list(filter(lambda unit: unit['unit_id'] == unit_id, self.units_summary))[0]
        if icon_type in [ICON_TYPE_EVENT_POINT_COUNT_NORMAL, ICON_TYPE_EVENT_POINT_RANKING_NORMAL]:
            card_id = unit['normal_card_id']
        if icon_type in [ICON_TYPE_EVENT_POINT_COUNT_IDOLIZED, ICON_TYPE_EVENT_POINT_RANKING_IDOLIZED]:
            card_id = unit['rank_max_card_id']
        unit_icon_url = urllib.parse.urljoin(SKUFES_CARD_IMAGE_DOMAIN, SKUFES_CARD_IMAGE_ENDPOINT + '%d.png' % card_id)
        response = requests.get(unit_icon_url)
        with open('static/images/icon_framed_%d_%d.png' % (event_id, icon_type), 'wb') as f:
            f.write(response.content)
    def processEventRewardUnit(self, event_detail: dict, icon_type: int):
        if icon_type in [ICON_TYPE_EVENT_POINT_COUNT_NORMAL, ICON_TYPE_EVENT_POINT_COUNT_IDOLIZED]:
            rewards_list = event_detail['event_point_counts']
        if icon_type in [ICON_TYPE_EVENT_POINT_RANKING_NORMAL, ICON_TYPE_EVENT_POINT_RANKING_IDOLIZED]:
            rewards_list = event_detail['event_point_rankings']
        for rewards in reversed(rewards_list):
            for reward in rewards['rewards']:
                if reward['image_display_flag'] == 1:
                    unit_id = reward['item_id']
                    self.getUnitIcon(unit_id, event_detail['event_id'], icon_type)
    def processEvent(self, event: dict):
        event_id = event['event_id']
        missing_icons = []
        for icon_type in ICON_TYPES:
            if not os.path.exists('static/images/icon_framed_%d_%d.png' % (event_id, icon_type)):
                missing_icons.append(icon_type)
        if len(missing_icons) != 0:
            event_detail_url = urllib.parse.urljoin(SKUFES_API_DOMAIN, SKUFES_API_EVENT_ENDPOINT + str(event_id))
            response = requests.get(event_detail_url)
            if response.status_code != 200:
                pass
            event_detail = response.json()
        for icon_type in missing_icons:
            self.processEventRewardUnit(event_detail, icon_type)
    def run(self):
        for event in self.events_summary:
            if event['event_id'] >= MINIMUM_EVENT_ID:
                self.processEvent(event)

if __name__ == '__main__':
    icon_getter = EventRewardUnitIconGetter()
    icon_getter.run()
