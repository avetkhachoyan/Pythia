// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract HumanLifeToken is ERC721Enumerable, Ownable {
    struct LifeEvent {
        string eventType;
        uint256 timestamp;
        string details;
    }

    struct HumanLife {
        string name;
        string birthDate;
        string birthPlace;
        string gender;
        LifeEvent[] events;
    }

    mapping(uint256 => HumanLife) public humanLives;
    mapping(address => bool) public hasConnected;

    event FirstTimeConnected(address indexed user);

    constructor() ERC721("HumanLifeToken", "HLT") Ownable(msg.sender) {}

    function mintFirstTimeToken(address to) public {
        require(!hasConnected[to], "Token already minted for this address");
        uint256 tokenId = totalSupply() + 1;
        _mint(to, tokenId);
        hasConnected[to] = true;
        emit FirstTimeConnected(to);
    }

    function addLifeEvent(uint256 tokenId, string memory eventType, uint256 timestamp, string memory details) public {
        require(ownerOf(tokenId) == msg.sender, "You do not own this token");
        humanLives[tokenId].events.push(LifeEvent(eventType, timestamp, details));
    }

    function setHumanLife(uint256 tokenId, string memory name, string memory birthDate, string memory birthPlace, string memory gender) public {
        require(ownerOf(tokenId) == msg.sender, "You do not own this token");
        
        delete humanLives[tokenId].events;
        
        HumanLife storage hl = humanLives[tokenId];
        hl.name = name;
        hl.birthDate = birthDate;
        hl.birthPlace = birthPlace;
        hl.gender = gender;
    }

    function getHumanLife(uint256 tokenId) public view returns (HumanLife memory) {
        return humanLives[tokenId];
    }

    function getLifeEvents(uint256 tokenId) public view returns (LifeEvent[] memory) {
        return humanLives[tokenId].events;
    }
}
