// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
 
contract SimpleStorage {
    // uint256 favoriteNumber = 5;
    // bool favoriteBool = false;
    // string favoriteString = "String";
    // int256 favoriteInt = -5;
    // bytes32 favoriteBytes = "cat";
 
    uint256 public favoriteNumber;
 
    struct People{
        uint favoriteNumber;
        string name;
    }
 
    People public person = People({favoriteNumber : 23, name : "Khushbu"});
 
    function store(uint256 _favoriteNumber) public{
        favoriteNumber = _favoriteNumber;
    }
 
    function retrieve() public view returns(uint256)
    {
        return favoriteNumber;
    }
 
    People[] public people;
    mapping(string=>uint256)public nameToFavoriteNumber;
    function addperson(string memory _name , uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name]=_favoriteNumber;
    }
 
}
 