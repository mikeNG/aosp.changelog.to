#include <stdio.h>
#include <string.h>

char currentProject[256];
char forkPoint[256];

void changeProject(char *line) {
	while(*line != '\0') {
		if(*line == '=') {
			line +=2;
			int position = 0;
			while(*line != '\0' && *line != '\n' && *line != '\r') {
				currentProject[position++] = *line;
				line++;
			}
			currentProject[position] = '\0';
			return;
		}	
		line++;
	}
}


void newProject(char *line, int *changeCount) {
	if(*changeCount > 0) {
		puts("</div></p>\n");
	}
	*changeCount = '\0';
	*forkPoint = '\0';
	changeProject(line);
}

void sanitiseProjectName(char *originalName, char *sanitisedName) {
	int position = 0;
	char c;
	while((c = originalName[position]) != '\0') {
		if(c == '/') {
			c = '_';
		}
		sanitisedName[position] = c;
		position++;
	}
	sanitisedName[position] = '\0';
}


void trimString(char *string) {
	while(*string != '\0' && *string >= 32) {
		string++;
	}
	*string = '\0';	
}

void writeChangeId(char *changeId) {
	trimString(changeId);
	fputs("<a href=\"", stdout);
	fputs("https://android.googlesource.com/", stdout);
	fputs(currentProject, stdout);
	fputs("/+/", stdout);
	fputs(changeId, stdout);
	fputs("\">", stdout);
	fputs(changeId, stdout);
	fputs("</a>", stdout);	
}

void writeForkPoint() {	
	fputs("Forked at : ", stdout);
	writeChangeId(forkPoint);
	fputs("\n\n", stdout);
}


void displayProjectName() {    
	char sanitisedName[256];
	sanitiseProjectName(currentProject, sanitisedName);
	
	fputs("<p><h2>", stdout);	
	fputs("<a href=\"#\" id=\"", stdout);
	fputs(sanitisedName, stdout);
	fputs("-show\" class=\"showLink\" onclick=\"show('", stdout);
	fputs(sanitisedName, stdout);
	fputs("');return false;\">+</a>", stdout);
	fputs("<a href=\"#\" id=\"", stdout);
	fputs(sanitisedName, stdout);
	fputs("-hide\" class=\"hideLink\" onclick=\"hide('", stdout);
	fputs(sanitisedName, stdout);
	fputs("');return false;\">-</a>", stdout);
	fputs("&nbsp;<a name=\"", stdout);
	fputs(sanitisedName, stdout);
	fputs("\" class=\"nonLink\">Project:</a> <a href=\"", stdout);
	fputs("https://android.googlesource.com/", stdout);
	fputs(currentProject, stdout);
	fputs("\">", stdout);
	fputs(currentProject, stdout);
	fputs("</a></h2>\n", stdout);	
	fputs("<div id=\"", stdout);
	fputs(sanitisedName, stdout);
	fputs("\">", stdout);

	if(*forkPoint != '\0') {
		writeForkPoint();
	}
}

void mergeBase(char *line) {
	int position = 0;
	while(line[position] != '=') {
		if(line[position] == '\0') {
			return;
		}
		position++;
	}
	
	position++;
	int i;
	for(i = 0; line[position] >= 32 ; i++, position++) {
		forkPoint[i] = line[position];
	}
	forkPoint[i] = '\0';
}

void newChange(char *line, int *changeCount) {
	if(*changeCount == 0) {
		displayProjectName();
	}
	
	(*changeCount)++;
	
	char changeId[256];
	int position=0;
	while(*line != ' ') {
		changeId[position++] = *line;
		line++;
	}
	changeId[position]='\0';

	writeChangeId(changeId);	
	fputs(" : ", stdout);	
	
	while(*line != '\0' && *line != '\n' && *line !='\r') {
		if(*line == '<') {
			fputs("&lt;", stdout);
		} else if (*line == '>') {
			fputs("&gt;", stdout);
		} else if (*line == '&') {
			fputs("&amp;", stdout);
		} else {
			fputc(*line, stdout);
		}
		line++;
	}
	
	fputs("\n", stdout);
}

void processLine(char *line, int *changeCount) {
	while(*line == ' ' || *line == '\t') {
		line++;
	}
	if(line[0] == 'p') {
		newProject(line, changeCount);
	} else if(line[0] == 'm') {
		mergeBase(line);
	} else {
		newChange(line, changeCount);
	}
}

int main(int argc, char *argv[]) {

	char line[1024];
	int changeCount = 0;
	while( fgets(line, sizeof(line), stdin) != NULL ) {
		processLine(line, &changeCount);
	}
	if(changeCount > 0) {
		fputs("</div></p>", stdout);
	}

	return 0;
}

