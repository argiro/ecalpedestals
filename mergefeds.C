#include <TTree.h>
#include <TFile.h>
#include <glob.h>
#include <vector>
#include <string>

// merge Trees from the different feds into the same one
// root -b -q mergefeds.C

std::vector<std::string> glob(const std::string& pat){
    using namespace std;
    glob_t glob_result;
    glob(pat.c_str(),GLOB_TILDE,NULL,&glob_result);
    vector<string> ret;
    for(unsigned int i=0;i<glob_result.gl_pathc;++i){
        ret.push_back(string(glob_result.gl_pathv[i]));
    }
    globfree(&glob_result);
    return ret;
}


int mergefeds(){

    using namespace std;
    const unsigned int nchs = 75848;
    int timestamp=0;
    int run=0;
    float lped[nchs];
    float lpedrms[nchs];

    vector<TTree * > trees;

    
    vector<string> rfiles = glob("new/pedestals_fed???_??????_??????.root");

    for (auto const fname:rfiles){
        TFile * curfile = new TFile(fname.c_str());
        TTree * curtree = dynamic_cast<TTree*> (curfile->Get("peds"));
        trees.push_back(curtree);
    }

    TFile rfile("mergedtree.root","recreate");
    TTree tree("peds","pedestals");
    tree.Branch("timestamp",&timestamp,"timestamp/I");
    tree.Branch("run",&run,"run/I");
    tree.Branch("lped",&lped,"lped[75848]/F");
    tree.Branch("lpedrms",&lpedrms,"lpedrms[75848]/F");

    int tmptimestamp;
    int tmprun;
    float tmplped[nchs];
    float tmplpedrms[nchs];

    for (int evno=0; evno< trees[0]->GetEntries();++evno){

        trees[0]->SetBranchAddress("timestamp",&tmptimestamp);
        trees[0]->SetBranchAddress("run",&tmprun);
        trees[0]->SetBranchAddress("lped",&tmplped);
        trees[0]->SetBranchAddress("lpedrms",&tmplpedrms);

        trees[0]->GetEntry(evno);
        
        //cout << "Timestamp " << tmptimestamp<< endl;
        
        for (auto curtree:trees){
            curtree->SetBranchAddress("timestamp",&tmptimestamp);
            curtree->SetBranchAddress("run",&tmprun);
            curtree->SetBranchAddress("lped",&tmplped);
            curtree->SetBranchAddress("lpedrms",&tmplpedrms);
            curtree->GetEntry(evno);

            //for (i =0; i<nchs; ++i) cout<< i << " " <<tmplped[i]<< " ";

            for (unsigned int idx=0; idx<nchs; ++idx){

                if (tmplped[idx] >0){ 
                    lped[idx] = tmplped[idx];
                    lpedrms[idx] = tmplpedrms[idx];
                    //cout << idx << " " << lped[idx] << " "<< endl;
                }
            }
        }
        run = tmprun;
        timestamp= tmptimestamp;
        tree.Fill();
    }
    tree.Write();
    return 0;
};
