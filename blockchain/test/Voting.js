const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Voting", function () {
  let voting;

  beforeEach(async function () {
    const Voting = await ethers.getContractFactory("Voting");
    voting = await Voting.deploy();
  });

  it("Should cast a vote", async function () {
    await voting.castVote(1, 1, 1);
    expect(await voting.getVoteCount(1, 1)).to.equal(1);
  });

  it("Should prevent double voting", async function () {
    await voting.castVote(1, 1, 1);
    await expect(voting.castVote(1, 1, 1)).to.be.revertedWith("User already voted");
  });

  it("Should check voted status", async function () {
    await voting.castVote(1, 1, 1);
    expect(await voting.checkVoted(1, 1)).to.equal(true);
  });
});