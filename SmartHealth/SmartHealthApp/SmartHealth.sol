pragma solidity >= 0.8.11 <= 0.8.11;

contract SmartHealth {
    string public hospital_details;
    string public patient_details;
    string public prescription;
    string public disease;

    //call this function to save disease data to Blockchain
    function setDisease(string memory d) public {
       disease = d;	
    }
   //get disease details
    function getDisease() public view returns (string memory) {
        return disease;
    }
       
    //call this function to save hospital data to Blockchain
    function setHospital(string memory hd) public {
       hospital_details = hd;	
    }
   //get hospital details
    function getHospital() public view returns (string memory) {
        return hospital_details;
    }

    //call this function to save patient data to Blockchain
    function setPatient(string memory pd) public {
       patient_details = pd;	
    }
   //get hospital details
    function getPatient() public view returns (string memory) {
        return patient_details;
    }

    //call this function to save prescription data to Blockchain
    function setPrescription(string memory p) public {
       prescription = p;	
    }
   //get hospital details
    function getPrescription() public view returns (string memory) {
        return prescription;
    }

    constructor() public {
        hospital_details="";
	prescription = "";
	patient_details="";
	disease = "";
    }
}