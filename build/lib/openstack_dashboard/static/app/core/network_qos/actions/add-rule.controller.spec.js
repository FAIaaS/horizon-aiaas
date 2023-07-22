/*
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

(function() {
  'use strict';

  describe('qos rules datails', function() {

    var ctrl, rules, directions, ppsDirections, $controller, $scope,
      $rootScope, dscp, minBwd, nminBwd, bwdLmt, nbwdLmt, minPckRt,
      nminPckRt;

    beforeEach(module('horizon.app.core.network_qos'));

    beforeEach(inject(function(_$controller_, _$rootScope_) {
      $controller = _$controller_;
      $rootScope = _$rootScope_;
      $scope = $rootScope.$new();

      $scope = {
        model: {
          qospolicy: "1",
          qospolicyname: "test-qos"
        }
      };

      ctrl = $controller('horizon.app.core.network_qos.actions.AddQoSRuleController',
        {
          $scope: $scope
        }
      );

      rules = {
        'bandwidth_limit': "Bandwidth Limit",
        'dscp_marking': "DSCP Marking",
        'minimum_bandwidth': "Minimum Bandwidth",
        'minimum_packet_rate': "Minimum Packet Rate"
      };
      directions = {
        "egress": "egress",
        "ingress": "ingress"
      };
      ppsDirections = {
        "egress": "egress",
        "ingress": "ingress",
        "any": "any"
      };
      dscp = {
        model: {
          dscpmarking: 0
        }
      };
      minBwd = {
        model: {
          minkbps: 1000,
          direction: 'egress'
        }
      };
      nminBwd = {
        model: {
          minkbps: 1000,
          direction: ''
        }
      };
      bwdLmt = {
        model: {
          maxkbps: 2000,
          maxburstkbps: 3000,
          direction: 'egress'
        }
      };
      nbwdLmt = {
        model: {
          maxkbps: 2000,
          maxburstkbps: 3000,
          direction: ''
        }
      };
      minPckRt = {
        model: {
          minkpps: 1000,
          direction: 'egress'
        }
      };
      nminPckRt = {
        model: {
          minkpps: 1000,
          direction: ''
        }
      };
    }));

    it('sets ctrl', inject(function() {
      expect(ctrl.qospolicy).toEqual($scope.model.qospolicy);
      expect(ctrl.qospolicy).not.toEqual('2');
      expect(ctrl.qospolicyname).toEqual($scope.model.qospolicyname);
      expect(ctrl.rule_types).toEqual(rules);
      ctrl.onRuleTypeChange('dscp_mark');
      expect(ctrl.onRuleTypeChange).toBeDefined();
      expect(ctrl.directions).toEqual(directions);
      expect(ctrl.ppsDirections).toEqual(ppsDirections);
      ctrl.onDSCPChange(dscp.model);
      expect(ctrl.onDSCPChange).toBeDefined();
      ctrl.minBandwidth(minBwd.model);
      expect(ctrl.minBandwidth).toBeDefined();
      ctrl.minBandwidth(nminBwd.model);
      expect(ctrl.minBandwidth).toBeDefined();
      ctrl.bwdLimit(bwdLmt.model);
      expect(ctrl.bwdLimit).toBeDefined();
      ctrl.bwdLimit(nbwdLmt.model);
      expect(ctrl.nbwdLimit).not.toBeDefined();
      ctrl.minPacketRate(minPckRt.model);
      expect(ctrl.minPacketRate).toBeDefined();
      ctrl.minPacketRate(nminPckRt.model);
      expect(ctrl.minPacketRate).toBeDefined();
    }));

  });
})();
