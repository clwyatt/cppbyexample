#include <cstdlib>
#include <cctype>
#include <fstream>
using std::ifstream;

#include <string>
using std::string;

#include <iostream>
using std::cout;
using std::endl;

#include <vector>
using std::vector;

bool isempty(const string & line)
{
  for(string::const_iterator it = line.begin();
      it != line.end(); ++it)
    {
      if( !isspace(*it) ) return false;
    }

  return true;
}

// test if line starts with //
bool iscomment(const string & line)
{
  bool toggle = false;
  for(string::const_iterator it = line.begin();
      it != line.end(); ++it)
    {
      if( isspace(*it) ) continue;
      if( (*it == '/') && !toggle ) toggle = true;
      if( (*it == '/') && toggle ) return true;
      if( (*it != '/') && toggle ) toggle = false;
    }
  return false;
}

void trim_comment_front(string & line)
{
  unsigned int count = 2;
  for(string::const_iterator it = line.begin();
      it != line.end(); ++it)
    {
      if( isspace(*it) ) count += 1;
      else break;
    }

  line.erase( line.begin(), line.begin() + count );
}

struct BlockType
{
  bool docblock;
  vector<string> lines;
};

void parse_example(const string & exname, vector<BlockType> & blocks)
{
  string path = "examples/" + exname + "/";
  path = path + exname + ".cc";
  ifstream exstr(path.c_str());

  BlockType blk;
  blk.docblock = true;
  while( !exstr.eof() )
    {
      string line;
      getline(exstr, line);
      cout << line.c_str() << endl;
      bool comment = iscomment(line);
      if( blk.docblock == true && comment )
	{
	  trim_comment_front(line);
	  blk.lines.push_back(line);
	  continue;
	}
      if( blk.docblock == true && !comment )
	{
	  blocks.push_back(blk);
	  blk.lines.clear();
	  blk.docblock = false;
	  blk.lines.push_back(line);
	  continue;
	}
      if( blk.docblock == false && !comment )
	{
	  blk.lines.push_back(line);
	  continue;
	}
      if( blk.docblock == false && comment )
	{
	  blocks.push_back(blk);
	  blk.lines.clear();
	  blk.docblock = true;
	  trim_comment_front(line);
	  blk.lines.push_back(line);
	  continue;
	}
    }

  // close last block
  blocks.push_back(blk);
}

void parse_render_example(const string & exname)
{
  vector<BlockType> blocks;
  parse_example(exname, blocks);

  for( vector<BlockType>::iterator it = blocks.begin();
       it != blocks.end(); ++it)
    {
      if(it->docblock) cout << "BEGIN DOC BLOCK (" << it->lines.size() << " lines)" << endl;
      else cout << "BEGIN CODE BLOCK ("  << it->lines.size() << " lines)" << endl;
      for(vector<string>::iterator bit = it->lines.begin();
	  bit != it->lines.end(); ++bit)
	{
	  cout << bit->c_str() << endl;
	}
      if(it->docblock) cout << "END DOC BLOCK" << endl;
      else cout << "END CODE BLOCK" << endl;
    }
}

int main()
{
  ifstream examples("examples.txt");

  while(!examples.eof())
    {
      string line;
      getline(examples, line);

      if( !isempty(line) )
	{
	  parse_render_example(line);
	}
    }

  return EXIT_SUCCESS;
}
