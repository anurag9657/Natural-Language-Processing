import sys
import re
import math
import csv
from abc import ABCMeta, abstractmethod
from nltk.corpus import stopwords
from collections import Counter


class Classifier(metaclass=ABCMeta):
    
    # Function to Read file

    def __init__(self, filename):
        try:
            input_file = open(filename, 'r')
        except:
            print('Can\'t read file ' + input_file )
            sys.exit(1)

        self.words = set()  # Words Vocabulary
        self.countClasses = dict()  # Occurrence of each class
        self.totalClasses = 0  # Total number of classes
        self.countWords = dict()  # Count of each word in a class
        self.totalWords = dict()  # Count of total words in a class

        # Train the model
        self.train(input_file)

        input_file.close()  # close the file


    @abstractmethod
    def train(self, input_file):
        pass

    # Perform classification on the given document


    def classify(self, document):
        # Calculate probability for each class
        probability = -math.inf
        computedClass = None
        for _class in self.countClasses:
            # Calculate class probability
            classProbability = math.log(self.countClasses[_class] / self.totalClasses)

            # Calculate probability of words
            for word in document:
                if word in self.words:
                    wordCount = self.countWords[_class][word] if word in self.countWords[_class] else 0
                    classProbability += math.log(wordCount + 1) - math.log(self.totalWords[_class] + len(self.words))

            if classProbability > probability:
                probability = classProbability
                computedClass = _class

        return computedClass

    # 20 representative words

    def representative_words(self):
        rwords = dict()
        for _class in self.countWords:
            rwords[_class] = dict(Counter(self.countWords[_class]).most_common(20))
        return rwords


class naiveBayesClassifier(Classifier):
    def __init__(self, filename):
        self.name = 'Naive Bayes Classifier Accuracy'
        super().__init__(filename)

    def train(self, input_file):
        for line in input_file:
            # Remove all special characters except apostrophe
            line = re.sub(r"[^a-z0-9']", " ", line.strip())

            if not line:
                continue

            # Split words
            words = line.split()

            # Initialize class
            _class = words[0]
            words = words[1:]
            if _class not in self.countClasses:
                self.countClasses[_class] = 0
                self.countWords[_class] = dict()
                self.totalWords[_class] = 0

            self.countClasses[_class] += 1
            self.totalClasses += 1
            self.words.update(words)
            self.totalWords[_class] += len(words)
            for word in words:
                if word not in self.countWords[_class]:
                    self.countWords[_class][word] = 1
                else:
                    self.countWords[_class][word] += 1


class binaryNaiveBayesClassifier(Classifier):
    def __init__(self, filename):
        self.name = 'Binomial Naive Bayes Classifier'
        super().__init__(filename)

    def train(self, input_file):
        for line in input_file:
            # Remove all special characters except apostrophe
            line = re.sub(r"[^a-z0-9']", " ", line.strip())

            if not line:
                continue

            # Split words
            words = line.split()

            # Initialize class
            _class = words[0]
            words = set(words[1:])
            if _class not in self.countClasses:
                self.countClasses[_class] = 0
                self.countWords[_class] = dict()
                self.totalWords[_class] = 0

            self.countClasses[_class] += 1
            self.totalClasses += 1
            self.words.update(words)
            self.totalWords[_class] += len(words)
            for word in words:
                if word not in self.countWords[_class]:
                    self.countWords[_class][word] = 1
                else:
                    self.countWords[_class][word] += 1


class withoutStopClassifier(Classifier):
    def __init__(self, filename):
        self.name = 'Naive Bayes Classifier Accuracy without stopwords'
        super().__init__(filename)

    def train(self, input_file):
        self.stopwords = stopwords.words('english')

        for line in input_file:
            # Remove all special characters except apostrophe
            line = re.sub(r"[^a-z0-9']", " ", line.strip())

            if not line:
                continue

            # Split words
            words = line.split()

            # Initialize class
            _class = words[0]
            words = words[1:]

            # Ignoring stop words
            words = [word for word in words if word not in self.stopwords]
            if _class not in self.countClasses:
                self.countClasses[_class] = 0
                self.countWords[_class] = dict()
                self.totalWords[_class] = 0

            self.countClasses[_class] += 1
            self.totalClasses += 1
            self.words.update(words)
            self.totalWords[_class] += len(words)
            for word in words:
                if word not in self.countWords[_class]:
                    self.countWords[_class][word] = 1
                else:
                    self.countWords[_class][word] += 1

    def classify(self, document):
        # Remove stop words from the document
        document = [word for word in document if word not in self.stopwords]
        # Call method of super class
        return super().classify(document)


def execute_classification(classifier, filename):
    # Read file
    try:
        input_file = open(filename, 'r')
    except:
        print('Could not open file ' + filename)
        sys.exit(1)

    totalCount = 0
    correctCount = 0

    for line in input_file:
        line = re.sub(r"[^a-z0-9']", " ", line.strip())
        if not line:
            continue

        words = line.split()
        givenClass = words[0]
        computedClass = classifier.classify(words[1:])
        if computedClass == givenClass:
            correctCount += 1
        totalCount += 1

    # Calculate accuracy
    accuracy = correctCount * 100 / totalCount
    print('%-37s' % classifier.name)
    print('Accuracy: %26.2f%%' % accuracy)
    print("\n")
    input_file.close()


def write_representative_words(classifier, filename):
    # Open file for writing
    try:
        output_file = open(filename, 'w')
    except:
        print('Could not open file ' + filename)
        sys.exit(1)

    rwords = classifier.representative_words()

    fieldnames = ['Speaker', 'Word', 'Frequency']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    for _class in rwords:
        for word in rwords[_class]:
            writer.writerow({'Speaker': _class, 'Word': word, 'Frequency': rwords[_class][word]})

    output_file.close()

# Initialize and train classifier
classifier = naiveBayesClassifier('train')

# Classify dev set
execute_classification(classifier, 'dev')

# Classify test set
execute_classification(classifier, 'test')

# Write representative words
write_representative_words(classifier, 'naiveBayesClassifier.csv')

# Initialize and train classifier
classifier = binaryNaiveBayesClassifier('train')

# Classify dev set
execute_classification(classifier, 'dev')

# Classify test set
execute_classification(classifier, 'test')

# Write representative words
write_representative_words(classifier, 'binomialNaiveBayes.csv')

# Initialize and train classifier
classifier = withoutStopClassifier('train')

# Classify dev set
execute_classification(classifier, 'dev')

# Classify test set
execute_classification(classifier, 'test')

# Write representative words
write_representative_words(classifier, 'naiveBayesWithoutStop.csv')
