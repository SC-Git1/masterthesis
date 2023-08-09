## this script takes in two arguments: 1) location of a protein file and 2) percentage to calculate an estimate for

suppressMessages(library(Peptides))
suppressMessages(library(Biostrings))
suppressMessages(library(stringr))
suppressMessages(library(robustbase))


Scalesfun <- function(filepath,perc) {

  # read in the sequences
  AA <- readAAStringSet(filepath, format="fasta")
  names <- names(AA)
  AAchar0 <- as.character(AA, use.names = FALSE)
  # remove wrong AAs
  AAchar <- gsub("[UXOB]", "", AAchar0)


  for (seq in AAchar) {
    # subset the protein
    len <- str_length(seq)
    N <- ceiling(len*as.numeric(perc)/100)
    seq <- substr(seq, 1, N)
    # calculate the scales
    scales <- cbind(do.call(rbind, unname(cbind(kideraFactors(seq)))),do.call(rbind, unname(cbind(tScales(seq)))), do.call(rbind, unname(cbind(stScales(seq)))),
       do.call(rbind, unname(cbind(blosumIndices(seq)))), do.call(rbind, unname(cbind(zScales(seq)))), do.call(rbind, unname(cbind(mswhimScores(seq)))),
       do.call(rbind, unname(cbind(vhseScales(seq)))), do.call(rbind, unname(cbind(fasgaiVectors(seq)))), do.call(rbind, unname(cbind(crucianiProperties(seq)))))
    
    # write to file
    logFile <- "StabilitySubsetAA_all.csv"
    cat(c(names[1],as.character(perc),""), file=logFile, append=TRUE, sep = ",")
    names <- names[-1]
    cat(unlist(scales), file=logFile, append=TRUE, sep = ",")
    cat('\n', file=logFile, append=TRUE)
  }
}


dirfile <- commandArgs(TRUE)[1]
perc <- commandArgs(TRUE)[2]
Scalesfun(dirfile,perc)


