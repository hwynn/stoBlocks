#include <iostream>
#include <string>
#include <fstream>
#include <vector>


#define DEBUG
//https://stackoverflow.com/questions/6444842/efficient-way-to-check-if-stdstring-has-only-spaces
bool isLineBlank(std::string line)
{
	return((line.find_first_not_of(" \t\n\v\f\r") == std::string::npos) ? true : false);
}

std::vector<std::string> extractAligned(std::string filename)
{
	std::ifstream our_file (filename);
	std::string temp;
	std::vector<std::string> aligned;
	if (our_file.is_open())
	{
		temp = "";
		getline(our_file, temp);
		
		
		getline(our_file, temp, '\n');
		for(size_t i=0; i<temp.length(); i++) //checking to see if getline accidently picked up entire file
			if(temp[i] == '\n')
			{
				std::cout << "Error: getline accidentally picked up the entire file" << std::endl;
				return aligned;
			}
		
		while(temp[0]=='#' or isLineBlank(temp))
		{
			getline(our_file, temp, '\n');
			//break and exit if we hit end of file //debug point
		}
		//debug point. check if temp starts with alphanumeric characters. it should.
		#ifdef DEBUG
			std::cout << "This should be alphanumeric: " << temp[0] << std::endl << std::endl;
		#endif
		
		
		aligned.push_back(temp.substr(17, temp.length())); //check if this accidentally includes characters before or after the cutoff point in the line.
		#ifdef DEBUG
			std::cout << "Check if this substring is getting what we need: " << std::endl;
			std::cout << "full line, substring: " << std::endl;
			std::cout << temp << std::endl << aligned[0] << std::endl << std::endl;
		#endif
		
		getline(our_file, temp, '\n');
		while(!(isLineBlank(temp)) and temp[0]!='/')
		{
			aligned.push_back(temp.substr(17, temp.length()));
			getline(our_file, temp, '\n');
		}
		//debug point. all items in aligned should have same length
		#ifdef DEBUG
		if(aligned.size() >= 2)
		{std::cout << "These should be the same: " << aligned[0].length() << ", "<< aligned[1].length() << std::endl << std::endl;}
		#endif
		
		int n = aligned.size();

		while(temp[0]!='/') //maybe check to see if we hit end of file
		{
			for(size_t i=0;i<(n-1); i=i+1)
			{
				getline(our_file, temp, '\n');
				aligned[i] = aligned[i] + (temp.substr(17, temp.length())); //or possibly aligned[i].push_back(temp[18:]);
			}
			getline(our_file, temp, '\n');
			//debug point. Temp should not contain alphanumeric characters at this poit. It should only contain whitespace or "//".
			#ifdef DEBUG
			std::cout << "This should be blank or //: " << temp << std::endl << std::endl;
			#endif
		}
		//debug point. all items in alignment should have same length
		#ifdef DEBUG
		if(aligned.size() >= 2)
		{std::cout << "These should be the same: " << aligned[0].length() << ", "<< aligned[1].length() << std::endl << std::endl;}
		#endif
	}
	else
	{
		std::cout << "Error: file could not be opened" << std::endl;
	}
	our_file.close();
	return aligned;
}


//int getEntropy(std::vector<char> xList) 

//std::vector<std::vector<int>> findBlocks (vector<int> scores, float max)

//std::vector<std::vector<std::string>> getBlocks(std::vector<std::vector<int>> places, std::vector<std::string> source)

int main ( int argc, char *argv[] )
{
	std::vector<std::string> aligned;
	if(argc > 1)
		aligned = extractAligned(argv[1]);
	else
		aligned = extractAligned("PF06306_full_length_sequences.sto");
	//debug point. check the length of alignment. It should not be 0.

	std::cout << "We have this many sequences: " << aligned.size() << std::endl;
	return 0;
}
