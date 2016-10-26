# Copyright (c) 2001-2014, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io

from __future__ import absolute_import, print_function, unicode_literals, division
from .tests_mechanism import AbstractTestFixture, config
from .check_utils import *
from .journey_common_tests import *


'''
This unit runs all the common tests in journey_common_tests.py.
'''

@config()
class TestJourneysDefault(JourneyCommon, AbstractTestFixture):

    def test_max_duration_equals_to_0(self):
        query = journey_basic_query + \
            "&first_section_mode[]=bss" + \
            "&first_section_mode[]=walking" + \
            "&first_section_mode[]=bike" + \
            "&first_section_mode[]=car" + \
            "&debug=true"
        response = self.query_region(query)
        check_journeys(response)
        eq_(len(response['journeys']), 4)

        query += "&max_duration=0"
        response = self.query_region(query)
        # the pt journey is eliminated
        eq_(len(response['journeys']), 3)

        # first is bike
        assert('non_pt_bike' == response['journeys'][0]['type'])
        eq_(len(response['journeys'][0]['sections']), 1)

        # second is empty
        assert('' == response['journeys'][1]['type'])
        eq_(len(response['journeys'][1]['sections']), 3)

        # last is bss
        assert('non_pt_bss' == response['journeys'][2]['type'])
        eq_(len(response['journeys'][-1]['sections']), 5)

    def test_journey_stop_area_to_stop_point(self):
        """
        When the departure is stop_area:A and the destination is stop_point:B belonging to stop_area:B
        """
        query = "journeys?from={from_sa}&to={to_sa}&datetime={datetime}"\
            .format(from_sa='stopA', to_sa='stop_point:stopB', datetime="20120614T080000")
        response = self.query_region(query)
        check_journeys(response)
        jrnys = response['journeys']

        j = next((j for j in jrnys if j['type'] == 'non_pt_walk'), None)
        assert j
        assert j['sections'][0]['from']['id'] == 'stopA'
        assert j['sections'][0]['to']['id'] == 'stop_point:stopB'
        assert j['type'] == 'non_pt_walk'


@config()
class TestJourneysNoRegionDefault(JourneysNoRegion, AbstractTestFixture):
    pass


@config()
class TestOnBasicRoutingDefault(OnBasicRouting, AbstractTestFixture):
    pass


@config()
class TestOneDeadRegionDefault(OneDeadRegion, AbstractTestFixture):
    pass


@config()
class TestWithoutPtDefault(WithoutPt, AbstractTestFixture):
    pass


@config()
class TestJourneysWithPtrefDefault(JourneysWithPtref, AbstractTestFixture):
    pass
