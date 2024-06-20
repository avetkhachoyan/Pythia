// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract HumanLifeToken is ERC721Enumerable, Ownable {
    constructor(address initialOwner) ERC721("HumanLifeToken", "HLT") Ownable(initialOwner) {
        transferOwnership(initialOwner);
    }

    struct LifeEvent {
        string eventType;
        uint256 timestamp;
    }

    struct Biography {
        string birthDate;
        string deathDate;
        string weddingDate;
        string divorceDate;
        string[] children;
        string education;
        LifeEvent[] events;
    }

    mapping(uint256 => Biography) private _biographies;
    mapping(uint256 => address) private _tokenOwners;

    event BiographyUpdated(uint256 tokenId, Biography biography);

    function mint(address to, uint256 tokenId, Biography memory biography) public onlyOwner {
        _safeMint(to, tokenId);
        _storeBiography(tokenId, biography);
        _tokenOwners[tokenId] = to;
    }

    function updateBiography(uint256 tokenId, Biography memory biography) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "HumanLifeToken: caller is not owner nor approved");
        require(_exists(tokenId), "HumanLifeToken: biography query for nonexistent token");
        _storeBiography(tokenId, biography);
        emit BiographyUpdated(tokenId, biography);
    }

    function getBiography(uint256 tokenId) public view returns (Biography memory) {
        require(_exists(tokenId), "HumanLifeToken: biography query for nonexistent token");
        return _biographies[tokenId];
    }

    function addLifeEvent(uint256 tokenId, LifeEvent memory lifeEvent) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "HumanLifeToken: caller is not owner nor approved");
        require(_exists(tokenId), "HumanLifeToken: add event query for nonexistent token");
        _biographies[tokenId].events.push(lifeEvent);
        emit BiographyUpdated(tokenId, _biographies[tokenId]);
    }

    function _storeBiography(uint256 tokenId, Biography memory biography) internal {
        // Clear the existing events array
        delete _biographies[tokenId].events;

        // Copy each LifeEvent from memory to storage
        for (uint256 i = 0; i < biography.events.length; i++) {
            _biographies[tokenId].events.push(biography.events[i]);
        }

        // Update other fields
        _biographies[tokenId].birthDate = biography.birthDate;
        _biographies[tokenId].deathDate = biography.deathDate;
        _biographies[tokenId].weddingDate = biography.weddingDate;
        _biographies[tokenId].divorceDate = biography.divorceDate;
        _biographies[tokenId].children = biography.children;
        _biographies[tokenId].education = biography.education;
    }

    function _isApprovedOrOwner(address spender, uint256 tokenId) internal view returns (bool) {
        require(_exists(tokenId), "ERC721: operator query for nonexistent token");
        address owner = ownerOf(tokenId);
        return (spender == owner || getApproved(tokenId) == spender || isApprovedForAll(owner, spender));
    }

    function _exists(uint256 tokenId) internal view returns (bool) {
        return _tokenOwners[tokenId] != address(0);
    }
}
