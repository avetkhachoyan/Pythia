// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract UnitEventRegistry {
    struct Unit {
        bytes32 id;
        mapping(string => uint) options;
    }

    struct Event {
        bytes32 id;
        string eventType;
        bytes32[] unitIds;
        uint timestamp;
    }

    mapping(bytes32 => Unit) public units;
    mapping(bytes32 => Event) public events;

    function addUnit(bytes32 unitId, string[] memory optionKeys, uint[] memory optionValues) public {
        require(optionKeys.length == optionValues.length, "Mismatched keys and values");
        Unit storage unit = units[unitId];
        unit.id = unitId;
        for (uint i = 0; i < optionKeys.length; i++) {
            unit.options[optionKeys[i]] = optionValues[i];
        }
    }

    function addEvent(bytes32 eventId, string memory eventType, bytes32[] memory unitIds, uint timestamp) public {
        Event storage evt = events[eventId];
        evt.id = eventId;
        evt.eventType = eventType;
        evt.unitIds = unitIds;
        evt.timestamp = timestamp;
    }
}
