suppressMessages(library(Peptides))
suppressMessages(library(Biostrings))
#suppressMessages(library(protr))
suppressMessages(library(robustbase))
suppressMessages(library(stringr))


Scalesfun <- function(filepath, perc, proteome) {

  AA <- readAAStringSet(filepath, format="fasta")
  AAchar0 <- as.character(AA, use.names = FALSE)
  
  # remove the sequences from length < 100 and percentile 99
  # So, first, remove all from percentile 99
  AAchar0lengths <- sapply(AAchar0, str_length, USE.NAMES = FALSE)
  q99 <- quantile(AAchar0lengths,0.99)
  AAchar0 <- AAchar0[sapply(AAchar0, function(i) {str_length(i) <= q99})]
  
  # remove incorrect AAs
  AAchar <- gsub("[UXOB]", "", AAchar0)

  # keep proteins of length > 100 AAs
  AAchar <- AAchar[sapply(AAchar, function(i) {str_length(i) >= 100})]

  # store the lengths after cleaning
  lenFile <- "LengthCleanedProteome.csv"
  cat(c(proteome, c(perc), c(length(AAchar))), file=lenFile, append=TRUE, sep = ",")
  cat('\n', file=lenFile, append=TRUE)

  # keep perc% of the proteins
  len <- length(AAchar)
  N <- ceiling(len*as.numeric(perc)/100)
  AAchar <- AAchar[1:N]

  # calculate the AA descriptors
  Listscales <- cbind(do.call(rbind, unname(cbind(kideraFactors(AAchar)))),do.call(rbind, unname(cbind(tScales(AAchar)))), do.call(rbind, unname(cbind(stScales(AAchar)))), 
     do.call(rbind, unname(cbind(blosumIndices(AAchar)))), do.call(rbind, unname(cbind(zScales(AAchar)))), do.call(rbind, unname(cbind(mswhimScores(AAchar)))), 
     do.call(rbind, unname(cbind(vhseScales(AAchar)))), do.call(rbind, unname(cbind(fasgaiVectors(AAchar)))), do.call(rbind, unname(cbind(crucianiProperties(AAchar))))) 
  
  # take the average and the mean
  scales <- c(colMeans(Listscales), colMedians(Listscales))

  # write to file
  logFile <- "StabilitySubsetProteome_all.csv"
  cat(c(proteome, c(perc), unlist(scales)), file=logFile, append=TRUE, sep = ",")
  cat('\n', file=logFile, append=TRUE)

}

# get all proteomes from a tab-delimited file with all assembly accessions
proteomes <- read.table(file = 'Proteomes.txt', sep = '\t', header = TRUE)

# iterate over all percentages
for (perc in 1:100) {
  for (proteome in proteomes[[1]]) {
    # read in the proteome
    Scalesfun(paste('/home/r0745770/Documents/AllProteomes/', proteome, ".faa", sep = ""), perc, proteome) 
  }
}

