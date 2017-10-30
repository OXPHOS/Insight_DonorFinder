Implementation of [Insight 2017 challenge](https://github.com/InsightDataScience/find-political-donors)

## Table of contents

- [Introduction](README.md#introduction)
- [Example](README.md#example)
- [Features](README.md#features)
    - [Work flow](README.md#work-flow)
    - [I/O](README.md#io)
        - [Input](README.md#input)
        - [Output](README.md#output)
    - [Data structure](README.md#data-structure)
        - [Low level data structure](README.md#low-level-data-structure)
        - [High level data structure](README.md#high-level-data-structure)
        - [Architecture](README.md#architecture)
- [Run instructions](README.md#run-instructions)
- [Testing](README.md#testing)

## Introduction

The project aims to identify possible donors to different candidates in election campaigns.

The scripts take in donation records regularly published by [Federal Election Commission](http://classic.fec.gov/finance/disclosure/ftpdet.shtml),
and analyze the data with stream-processing methods on single machine.

By running the package, one can get:

   - **Up-to-date calculated median, total dollar amount and total number of contributions to each candidate from different areas (zip codes)**, which reveals the areas (zip codes) that are optimal choices for soliciting future donations for similar candidates.
    
   - **Up-to-date calculated median, total dollar amount and total number of contributions to each candidate from different dates**, which hints the fundraising capacity of various fundraising events.

## Example

FEC provides donation records with fixed styles, such as (copied from [file](https://github.com/InsightDataScience/find-political-donors/blob/master/README.md#example)):

     C00629618|N|TER|P|201701230300133512|15C|IND|PEREZ, JOHN A|LOS ANGELES|CA|90017|PRINCIPAL|DOUBLE NICKEL ADVISORS|01032017|40|H6CA34245|SA01251735122|1141239|||2012520171368850783

     C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337

     C00384818|N|M2|P|201702039042412112|15|IND|ABBOTT, JOSEPH|WOONSOCKET|RI|028956146|CVS HEALTH|VP, RETAIL PHARMACY OPS|01122017|250||2017020211435-887|1147467|||4020820171370030285

     C00177436|N|M2|P|201702039042410893|15|IND|SABOURIN, JAMES|LOOKOUT MOUNTAIN|GA|307502818|UNUM|SVP, CORPORATE COMMUNICATIONS|01312017|230||PR1890575345050|1147350||P/R DEDUCTION ($115.00 BI-WEEKLY)|4020820171370029335

     C00177436|N|M2|P|201702039042410895|15|IND|JEROME, CHRISTOPHER|FALMOUTH|ME|041051896|UNUM|EVP, GLOBAL SERVICES|01312017|384||PR2283905245050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029342

     C00384818|N|M2|P|201702039042412112|15|IND|BAKER, SCOTT|WOONSOCKET|RI|028956146|CVS HEALTH|EVP, HEAD OF RETAIL OPERATIONS|01122017|333||2017020211435-910|1147467|||4020820171370030287

     C00177436|N|M2|P|201702039042410894|15|IND|FOLEY, JOSEPH|FALMOUTH|ME|041051935|UNUM|SVP, CORP MKTG & PUBLIC RELAT.|01312017|384||PR2283904845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029339

The records above contains [information](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml) about the recipients, donors and the donations.

For the purposes of this project, we will extract the information of recipients, and the donation (source, amount, date) from individuals, such as (copied from [file](https://github.com/InsightDataScience/find-political-donors/blob/master/README.md#example)):


      1.
      CMTE_ID: C00629618
      ZIP_CODE: 90017
      TRANSACTION_DT: 01032017
      TRANSACTION_AMT: 40
      OTHER_ID: H6CA34245

      2.
      CMTE_ID: C00177436
      ZIP_CODE: 30004
      TRANSACTION_DT: 01312017
      TRANSACTION_AMT: 384
      OTHER_ID: empty

      3. 
      CMTE_ID: C00384818
      ZIP_CODE: 02895
      TRANSACTION_DT: 01122017
      TRANSACTION_AMT: 250
      OTHER_ID: empty

      4.
      CMTE_ID: C00177436
      ZIP_CODE: 30750
      TRANSACTION_DT: 01312017
      TRANSACTION_AMT: 230
      OTHER_ID: empty

      5.
      CMTE_ID: C00177436
      ZIP_CODE: 04105
      TRANSACTION_DT: 01312017
      TRANSACTION_AMT: 384
      OTHER_ID: empty

      6.
      CMTE_ID: C00384818
      ZIP_CODE: 02895
      TRANSACTION_DT: 01122017
      TRANSACTION_AMT: 333
      OTHER_ID: empty

      7.
      CMTE_ID: C00177436
      ZIP_CODE: 04105
      TRANSACTION_DT: 01312017
      TRANSACTION_AMT: 384
      OTHER_ID: empty


- `CMTE_ID`: identification number of the recipient

- `ZIP_CODE`: area information of the donor (can be `N/A`)

- `TRANSACTION_DT`: date of the donation (can be `N/A`)

- `TRANSACTION_AMT`: amount of the donation

- `OTHER_ID`: other identification number to label non-individual donors

With analysis, the package will output two files:

- **`medianvals_by_zip.txt`**

  The calculated median, total dollar amount and total number of contributions to each candidate from different areas (zip codes).
  
  The scripts add a line of updated information to the output file with each valid record streaming in.

  The `medianvals_by_zip.txt` generated from the example input above is:

        C00177436|30004|384|1|384
        C00384818|02895|250|1|250
        C00177436|30750|230|1|230
        C00177436|04105|384|1|384
        C00384818|02895|292|2|583
        C00177436|04105|384|2|768

  with implicit header:

      Recipient's ID | Area (zip code) | Median of contribution | Total number of contributions | Total dollar amount of contributions |

- **`medianvals_by_date.txt`**

  The calculated median, total dollar amount and total number of contributions to each candidate from different dates.
  
  The [database](README.md#data-structure) keeps one entry for the summary of donation 
  to each recipient from each date. The entries are ordered by recipients' id number and the date.
  
   The `medianvals_by_date.txt` generated from the example input above is:
   
       C00177436|01312017|384|4|1382
       C00384818|01122017|292|2|583

  with implicit header:
  
       Recipient's ID | Date | Median of contribution | Total number of contributions | Total dollar amount of contributions |

## Features

### Work flow

                              Read record by streaming 
                                        |
                                        |
                                Check input inegrity
                                        |
                                        |
                  |--------------Update database--------------|
                  |                                           |
            (If zip code)                           (If transaction date)
                  |                                           |
                  |                                           |
    Stream out to medianvals_by_zip            Update the tree structure storing
                                       information grouped by indiviual and transaction date
                                                              |
                                                              |
                                         Output the updated ordered donation information
                                              grouped by indiviual and transaction date
                                                     to medianvals_by_date

### I/O
  The package require a single input file and two paths to store the outputs when executed.
  
#### Input
    
The scripts yield each line(record) reading from the input file. Before yielding, 
the [input methods](https://github.com/OXPHOS/Insight_DonorFinder/blob/master/src/stream_input.py) gurantee that
  - The entry is valid (by checking column number)
  - The recipient ID (`CMTE_ID`) is valid, which starts by 'C' followed by 8 digits
  - The transaction amount is valid number
  - Whether the zip code or the transaction date is valid
  
Also, the method converts the transaction amount to internal objects.
   
#### Output

As mentioned above, the output methods 
- append a new entry to `medianvals_by_zip.txt` if available
- re-order and re-write the `medianvals_by_date.txt` if available

The output files are header-free.

### Data structure

#### Low level data structure
  
  - **[`LinkedListNode`](https://github.com/OXPHOS/Insight_DonorFinder/blob/master/src/LinkedListNode.py)**
  
    Node of a doubly linked list. Wraps the value of transaction amount and provides access to other `LinkedListNode` objects with transaction amount just smaller and larger than the amount of current `LinkedListNode` object given grouping rule. The class is used for median search and update.
    
  - **[`InfoByDomainBase`](https://github.com/OXPHOS/Insight_DonorFinder/blob/master/src/InfoTable.py#L4) / (`InfoByZip` / `InfoByDate`)**
  
    Structure that saves median, counts and total dollar amount of contributions based on provided grouping rules. `InfoByZip` and `InfoByDate` are derived from `InfoByDomainBase`.
    
 #### High level data structure
   - **[`InfoIndividual`](https://github.com/OXPHOS/Insight_DonorFinder/blob/master/src/InfoTable.py#L154)**
    
     Basic data stroage structure in database that saves donation information received by each recipient. The object maintains two private dictionaries, with donations information grouped by zip codes and dates of the recipient (`InfoByZip`/`InfoByDate`).

   - **[`NodeBase`](https://github.com/OXPHOS/Insight_DonorFinder/blob/master/src/AVLTree.py#L1) / (`NodeByID` / `NodeByDate`)**
    
     Basic unit of self-balancing binary search tree, with the information of its children and its height in the tree. Allowing node `key_idx` comparison.
      - `NodeById`: use `int`-casted recipient ID as `key_idx` and saves all the information of donations (AVL Tree of `NodeByDate`) to one recipient
      - `NodeByDate`: use `int`-casted transaction date as `key_idx` and saves the information of donations to one recipient grouped by dates
      
   - **[`AVLTree`](https://github.com/OXPHOS/Insight_DonorFinder/blob/master/src/AVLTree.py#L114) / (`AVLTreeByID` / `AVLTreeByDate`)**
   
      Self-balanced binary search tree structure with nodes derived from `NodeBase`. Allowing dynamic and fast insertion of new records. Two `AVLTree` derived instances are used in the scripts:
      - **`AVLTreeByID`**: AVL Tree of each individual, ordered by recipient's ID numbers saved in `NodeByID`. Keys are converted to `int` for fast comparison. 
      - **`AVLTreeByDate`**: AVL Tree of dates, ordered by transaction dates saved in `NodeByDate`.
      
      The different derived classes only exist for different output requirement.
   
      Trees are in-order traversed during output.
   
#### Architecture
   - **Storage in database**
   
          infoDB
            └── InfoIndividual(id)
                   └── key: 
                       string(zip code)
                   └── value: 
                       infoByZip
                         └── int(median), int(count), float(total), 
                             [LinkedListNode(amount of each donation)]
                   └── key: 
                       string (transaction date)
                   └── value: 
                       infoByDate
                         └── int(median), int(count), float(total), 
                             [LinkedListNode(amount of each donation)]

   - **Storage in self-balanced binary search tree**    
    
            AVLTreeByID
             └── key_idx: 
                 int(casted recipient ID)
             └── value: 
                 AVLTreeByDate
                   └── key_idx: 
                       int (casted date)
                   └── value: 
                       infoByDate
                         └── int(median), int(count), float(total), 
                             [LinkedListNode(amount of each donation)]

## Run instructions

Your can run the package with test data in root folder by:

```
root~$ chmod +x run.sh
root~$ ./run.sh
```

Or run the package with your own input dataset by:

`root~$ ./run.sh path/to/input/file`
 
You can also change the output destination by specifying the output path. However, 
you must pass path to the input, and paths to both output files (groupby zip code output and groupby date output)
 at the same time.

`root~$ ./run.sh path/to/input/file ./run.sh path/to/medianvals_by_zip/output/file path/to/medianvals_by_date/output/file`

No external libraries or dependencies are required for execution.

The package is tested with Python 2.7.13 and Python 3.6.1.
  
## Testing

Two types of testing are implemented for the package.

### Module testing

Tests are supported by Python's `unittest` framework. The tests covering all modules from the package can be found in [`./tests/`](https://github.com/OXPHOS/Insight_DonorFinder/tree/master/tests). The tests can be run by:

`root~$ ./run-tests.sh`

### Structure and I/O testing

Enabled by Insight. Tests can be found under [`insight_testsuite/tests/`](https://github.com/OXPHOS/Insight_DonorFinder/tree/master/insight_testsuite/tests). To restrict the size of the package, not all test input/output files are uploaded.

The tests can be run by：

`insight_testsuite~$ ./run_tests.sh`
