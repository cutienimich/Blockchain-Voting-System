// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Voting {

    // ─── STRUCTS ─────────────────────────────────
    struct Vote {
        uint256 userId;
        uint256 electionId;
        uint256 candidateId;
        uint256 timestamp;
    }

    // ─── STATE ───────────────────────────────────
    address public owner;
    
    // electionId => userId => voted?
    mapping(uint256 => mapping(uint256 => bool)) public hasVoted;
    
    // electionId => candidateId => vote count
    mapping(uint256 => mapping(uint256 => uint256)) public voteCounts;
    
    // all votes stored
    Vote[] public votes;

    // ─── EVENTS ──────────────────────────────────
    event VoteCast(
        uint256 indexed electionId,
        uint256 indexed candidateId,
        uint256 indexed userId,
        uint256 timestamp
    );

    // ─── CONSTRUCTOR ─────────────────────────────
    constructor() {
        owner = msg.sender;
    }

    // ─── MODIFIER ────────────────────────────────
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    // ─── CAST VOTE ───────────────────────────────
    function castVote(
        uint256 _userId,
        uint256 _electionId,
        uint256 _candidateId
    ) external onlyOwner {
        // check not voted
        require(
            !hasVoted[_electionId][_userId],
            "User already voted"
        );

        // mark voted
        hasVoted[_electionId][_userId] = true;

        // count vote
        voteCounts[_electionId][_candidateId]++;

        // store vote
        votes.push(Vote({
            userId: _userId,
            electionId: _electionId,
            candidateId: _candidateId,
            timestamp: block.timestamp
        }));

        // emit event
        emit VoteCast(_electionId, _candidateId, _userId, block.timestamp);
    }

    // ─── GET VOTE COUNT ──────────────────────────
    function getVoteCount(
        uint256 _electionId,
        uint256 _candidateId
    ) external view returns (uint256) {
        return voteCounts[_electionId][_candidateId];
    }

    // ─── CHECK IF VOTED ──────────────────────────
    function checkVoted(
        uint256 _electionId,
        uint256 _userId
    ) external view returns (bool) {
        return hasVoted[_electionId][_userId];
    }

    // ─── GET TOTAL VOTES ─────────────────────────
    function getTotalVotes() external view returns (uint256) {
        return votes.length;
    }
}