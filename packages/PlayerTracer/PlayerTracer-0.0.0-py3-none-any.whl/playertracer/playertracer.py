import os
import sys
import beetools
import CsvWrpr
import DisplayFX
import FixDate
import rtutils

g_Version = '2.2.1'
g_ClassName = "PlayerTracer"
g_ClassDesc = "Trace players in a specific data set"


class PlayerTracer:
    def __init__(
        self,
        p_MemberDataPath,
        p_SourceData=None,
        p_SourceDataHeader=None,
        p_Silent=False,
        p_MemberDataHeader=None,
        p_MemberDataKey1='MemberId',
        p_MemberDataDelHead='MemberId',
    ):
        if p_SourceData is None:
            p_SourceData = []
        if p_SourceDataHeader is None:
            p_SourceDataHeader = []
        if p_MemberDataHeader is None:
            p_MemberDataHeader = [
                'Surname',
                'Init',
                'Name',
                'DOB',
                'Region',
                'MemberId',
                'Standard',
                'Gender',
                'Title',
                'Rapid',
                'Blitz',
            ]

        def expandMemberData():
            self.memberDataHeader = self.memberDataHeader + ['Surname', 'Name']
            for memberId in self.memberData:
                self.memberData[memberId]['Surname'] = self.memberData[memberId][
                    'SurnameName'
                ].split(',')[0]
                self.memberData[memberId]['Name'] = self.memberData[memberId][
                    'SurnameName'
                ].split(',')[1]
            pass

        self.addRating = False
        self.delimeter = ';'
        self.dOBSearchedDataIdx = 0
        self.exportData = []
        self.initMemberDataIdx = False
        self.madatoryFields = ['Name', 'Surname']
        self.memberDataHeader = p_MemberDataHeader
        self.memberDataPath = p_MemberDataPath
        self.memberDataIndexed = False
        self.memberDataKey1 = p_MemberDataKey1
        self.nameSearchedDataIdx = -1
        self.otherSearchFields = ['DOB', 'Year', 'Country', 'ChessaNr']
        self.sourceData = []
        self.sourceDataHeader = []
        self.silent = p_Silent
        self.smPlayersList = []
        self.surnameSearchedDataIdx = -1
        self.tracedPlayers = {}
        self.yearSearchedDataIdx = False
        self.memberData = CsvWrpr.CsvWrpr(
            self.memberDataPath,
            key1=p_MemberDataKey1,
            delHead=p_MemberDataDelHead,
            header=self.memberDataHeader,
            strucType='Dict',
            p_convertNone=False,
            silent=self.silent,
        ).csvDb.copy()
        if 'SurnameName' in self.memberDataHeader:
            expandMemberData()
        if p_SourceData:
            self.indexData(p_SourceData, p_SourceDataHeader)
            self.buildPriorityList()
        pass

    # end __init__

    def buildPriorityList(self):
        def findDOB(p_MemberData, p_MemberDataField, p_SearchedField):
            collection = []
            searchedFieldLen = len(p_SearchedField)
            for rec in p_MemberData:
                dataFieldLen = len(p_MemberData[rec][p_MemberDataField])
                if (searchedFieldLen == 8 and dataFieldLen == 8) or (
                    searchedFieldLen == 10 and dataFieldLen == 10
                ):
                    if p_SearchedField == p_MemberData[rec][p_MemberDataField]:
                        collection.append(rec)
                elif searchedFieldLen == 10 and dataFieldLen == 8:
                    if (
                        p_SearchedField == '19' + p_MemberData[rec][p_MemberDataField]
                        or p_SearchedField
                        == '20' + p_MemberData[rec][p_MemberDataField]
                    ):
                        collection.append(rec)
                elif searchedFieldLen == 8 and dataFieldLen == 10:
                    if (
                        '19' + p_SearchedField == p_MemberData[rec][p_MemberDataField]
                        or '20' + p_SearchedField
                        == p_MemberData[rec][p_MemberDataField]
                    ):
                        collection.append(rec)
            return collection

        # end findDOB

        def findHybridDOB(p_MemberData, p_MemberDataField, searchedField):
            collection = []
            searchedFieldLen = len(searchedField)
            for memberId in p_MemberData:
                dataFieldLen = len(p_MemberData[memberId][p_MemberDataField])
                searchYear = False
                dataYear = False
                searchMonth = False
                dataMonth = False
                searchDay = False
                dataDay = False
                if searchedFieldLen == 8 and dataFieldLen == 8:
                    searchYear = searchedField[:2]
                    dataYear = p_MemberData[memberId][p_MemberDataField][:2]
                    searchMonth = searchedField[3:5]
                    dataMonth = p_MemberData[memberId][p_MemberDataField][3:5]
                    searchDay = searchedField[6:]
                    dataDay = p_MemberData[memberId][p_MemberDataField][6:]
                elif searchedFieldLen == 10 and dataFieldLen == 10:
                    searchYear = searchedField[:4]
                    dataYear = p_MemberData[memberId][p_MemberDataField][:4]
                    searchMonth = searchedField[5:7]
                    dataMonth = p_MemberData[memberId][p_MemberDataField][5:7]
                    searchDay = searchedField[8:]
                    dataDay = p_MemberData[memberId][p_MemberDataField][8:]
                elif searchedFieldLen == 10 and dataFieldLen == 8:
                    searchYear = searchedField[:4]
                    dataYear = (
                        searchedField[:2]
                        + p_MemberData[memberId][p_MemberDataField][:2]
                    )
                    searchMonth = searchedField[5:7]
                    dataMonth = p_MemberData[memberId][p_MemberDataField][3:5]
                    searchDay = searchedField[8:]
                    dataDay = p_MemberData[memberId][p_MemberDataField][6:]
                elif searchedFieldLen == 8 and dataFieldLen == 10:
                    searchYear = p_MemberData[memberId][p_MemberDataField][:2]
                    dataYear = (
                        p_MemberData[memberId][p_MemberDataField][:2]
                        + searchedField[:2]
                    )
                    searchMonth = searchedField[3:5]
                    dataMonth = p_MemberData[memberId][p_MemberDataField][5:7]
                    searchDay = searchedField[6:]
                    dataDay = p_MemberData[memberId][p_MemberDataField][8:]
                matchCount = 0
                if searchYear == dataYear:
                    matchCount += 1
                if searchMonth == dataMonth:
                    matchCount += 1
                if searchDay == dataDay:
                    matchCount += 1
                if searchMonth == dataDay and searchDay == dataMonth:
                    matchCount += 1
                if (searchYear == dataYear and searchMonth == dataDay) or (
                    searchYear == dataYear and searchDay == dataMonth
                ):
                    matchCount += 1
                if matchCount >= 2:
                    collection.append(p_MemberData[memberId])
            return collection

        # end findHybridDOB

        def findMatches(
            p_MemberData,
            p_MemberDataField,
            p_SearchedField,
            p_MemberDataFieldSlice=None,
        ):
            if p_MemberDataFieldSlice is None:
                p_MemberDataFieldSlice = []
            collection = {}
            for memberId in p_MemberData:
                if not p_MemberDataFieldSlice:
                    if (
                        p_SearchedField.upper()
                        == p_MemberData[memberId][p_MemberDataField].upper()
                    ):
                        # collection[memberId]= p_MemberData[memberId].copy() # This has to be implemented because the "Priority" does not work correctly
                        collection[memberId] = p_MemberData[memberId]
                else:
                    if (
                        p_SearchedField.upper()
                        == p_MemberData[memberId][p_MemberDataField][
                            p_MemberDataFieldSlice[0] : p_MemberDataFieldSlice[1]
                        ].upper()
                    ):
                        # collection[memberId]= p_MemberData[memberId].copy() # This has to be implemented because the "Priority" does not work correctly
                        collection[memberId] = p_MemberData[memberId]
            return collection

        # end findMatches

        def findYear(p_MemberData, p_MemberDataField, searchedField):
            collection = []
            for memberId in p_MemberData:
                dataFieldYear = FixDate.FixDate(
                    p_MemberData[memberId][p_MemberDataField]
                ).year
                if searchedField == dataFieldYear:
                    collection.append(memberId)
            return collection

        # end findYear

        def prioritiseEntries(searchRec):
            def findRec(collection, memberId):
                found = False
                # i = 0
                if memberId in collection:
                    found = True
                return found

            # end prioritiseEntries

            priorityList = [[], [], [], [], []]
            nameFound = False
            nameInitFound = False
            nameShortFound = False
            dOBFound = False
            dobHybridFound = False
            yearFound = False
            for memberId in surnameCollection:
                nameFound = findRec(nameCollection, memberId)
                nameInitFound = findRec(nameInitCollection, memberId)
                initFound = findRec(initCollection, memberId)
                nameShortFound = findRec(nameShortCollection, memberId)
                dOBFound = findRec(dOBCollection, memberId)
                dobHybridFound = findRec(dOBHybridCollection, memberId)
                yearFound = findRec(yearCollection, memberId)
                if nameFound and dOBFound:
                    surnameCollection[memberId]['Priority'] = 0
                    priorityList[0].append(memberId)
                elif (
                    (nameInitFound or nameShortFound or initFound)
                    and (dOBFound or dobHybridFound)
                ) or (nameFound and (dobHybridFound or yearFound)):
                    surnameCollection[memberId]['Priority'] = 1
                    priorityList[1].append(memberId)
                elif dOBFound:
                    surnameCollection[memberId]['Priority'] = 2
                    priorityList[2].append(memberId)
                elif nameFound:
                    surnameCollection[memberId]['Priority'] = 3
                    priorityList[3].append(memberId)
                elif nameInitFound or nameShortFound or initFound:
                    surnameCollection[memberId]['Priority'] = 4
                    priorityList[4].append(memberId)
            self.tracedPlayers[searchRec] = []
            # priority = 0
            for priorityRec in priorityList:
                for rec in priorityRec:
                    self.tracedPlayers[searchRec].append(rec)

        # end prioritiseEntries

        listLen = len(self.sourceData)
        if not self.silent:
            print('Build priority list ({})'.format(listLen))
        dFX = DisplayFX.DisplayFX(
            intVal=0.20, defSet=3, sep='%', filler=1, silent=self.silent
        )
        for fxCntr, searchRec in enumerate(self.sourceData):
            surnameCollection = findMatches(
                self.memberData, 'Surname', searchRec[self.surnameSearchedDataIdx]
            )
            nameCollection = findMatches(
                surnameCollection, 'Name', searchRec[self.nameSearchedDataIdx]
            )
            if searchRec[self.nameSearchedDataIdx]:
                # Look if the first letter of the source name is the member name
                nameInitCollection = findMatches(
                    surnameCollection, 'Name', searchRec[self.nameSearchedDataIdx][0]
                )
            else:
                nameInitCollection = []
            if self.initMemberDataIdx:
                # look if the first letter of the source name is the initial
                initCollection = findMatches(
                    surnameCollection,
                    'Init',
                    searchRec[self.nameSearchedDataIdx][0],
                    p_MemberDataFieldSlice=[0, 1],
                )
            else:
                initCollection = []
            nameShortCollection = findMatches(
                surnameCollection,
                'Name',
                searchRec[self.nameSearchedDataIdx],
                p_MemberDataFieldSlice=[0, 1],
            )
            dOBCollection = []
            dOBHybridCollection = []
            yearCollection = []
            if self.dOBSearchedDataIdx:
                dOBCollection = findDOB(
                    surnameCollection, 'DOB', searchRec[self.dOBSearchedDataIdx]
                )
                if not dOBCollection:
                    dOBHybridCollection = findHybridDOB(
                        surnameCollection, 'DOB', searchRec[self.dOBSearchedDataIdx]
                    )
            if self.yearSearchedDataIdx:
                yearCollection = findYear(
                    surnameCollection, 'DOB', searchRec[self.yearSearchedDataIdx]
                )
            prioritiseEntries(searchRec[0])
            dFX.prNext(fxCntr / listLen)
        dFX.prFin()
        # check for '1900/01/01 DOB
        # Check for name and surname switched
        # check for spelling mistakes

    # end buildPriorityList

    def exportToCsv(self, path):
        exportFile = open(path, 'w', encoding='utf-8', errors='ignore')
        listLen = len(self.exportData)
        print('Export to CSV ({})'.format(listLen))
        dFX = DisplayFX.DisplayFX(intVal=0.20, defSet=3, sep='%', filler=1)
        for fxCntr, rec in enumerate(self.exportData):
            for i in range(len(rec)):
                if i == 0:
                    exportStr = '{}\n'.format(
                        self.delimeter.join([str(x) for x in rec[0]])
                    )
                else:
                    exportStr = '{}\n'.format(
                        self.delimeter.join(
                            [
                                str(self.memberData[rec[i]][field])
                                for field in self.memberData[rec[i]]
                            ]
                        )
                    )
                exportFile.write(exportStr)
            exportFile.write('\n')
            dFX.prNext(fxCntr / listLen)
        dFX.prFin()
        exportFile.close()

    # end exportToCsv

    def exportToSM(self, p_Path, p_AddRating=False):
        c_SearchedIDNo = 4
        c_RatingNat = 5
        duplicates = []
        self.smPlayersList = []
        self.addRating = p_AddRating
        exportHeader = '{}\n'.format(
            self.delimeter.join([str(x) for x in self.sourceDataHeader])
        )
        duplicatesPath = p_Path.replace('.', ' - Duplicates.')
        duplicatesFile = open(duplicatesPath, 'w', encoding='utf-8', errors='ignore')
        exportFile = open(p_Path, 'w', encoding='utf-8', errors='ignore')
        exportFile.write(exportHeader)
        listLen = len(self.exportData)
        print('Export to SM ({})'.format(listLen))
        # dFX = DisplayFX.DisplayFX(intVal=0.20, defSet=3, sep='%', filler=1)
        for fxCntr, exportSet in enumerate(self.exportData):
            newRow = exportSet[0]
            if len(exportSet) > 1:
                if self.memberData[exportSet[1]]['Priority'] <= 2:
                    newRow[c_SearchedIDNo] = exportSet[1]
                    if self.addRating:
                        newRow[c_RatingNat] = self.memberData[exportSet[1]]['Standard']
            exportStr = '{}\n'.format(self.delimeter.join([str(x) for x in newRow[1:]]))
            if newRow[c_SearchedIDNo] not in duplicates:
                if newRow[
                    c_SearchedIDNo
                ]:  # Blanks should not be added to the duplicate list
                    duplicates.append(newRow[c_SearchedIDNo])
                self.smPlayersList.append(newRow)
                exportFile.write(exportStr)
            else:
                duplicatesFile.write(exportStr)
        duplicatesFile.close()
        exportFile.close()

    # end exportToSM

    def findMemberId(self, detail):
        searchedData = [[]]
        searchedDataHeader = []
        self.exportData = []
        self.sourceData = []
        self.sourceDataHeader = []
        self.tracedPlayers = {}
        for field in self.madatoryFields:
            searchedData[0].append(detail[field])
            searchedDataHeader.append(field)
        for field in self.otherSearchFields:
            if field in detail:
                searchedData[0].append(detail[field])
                searchedDataHeader.append(field)
        tSilent = self.silent
        self.silent = True
        self.indexData(searchedData, searchedDataHeader)
        self.buildPriorityList()
        self.silent = tSilent
        if self.tracedPlayers[0]:
            MemberId = self.tracedPlayers[0][0]
        else:
            MemberId = ''
        return MemberId

    # end findMemberId

    def getBestMatch(self):
        self.exportData = []
        listLen = len(self.tracedPlayers)
        if not self.silent:
            print('Generate best match ({})'.format(listLen))
        dFX = DisplayFX.DisplayFX(
            intVal=0.20, defSet=3, sep='%', filler=1, silent=self.silent
        )
        for fxCntr, seq in enumerate(sorted(self.tracedPlayers)):
            row = [[seq] + self.sourceData[int(seq)][1:]]
            if self.tracedPlayers[seq]:
                row.append(self.tracedPlayers[seq][0])
            self.exportData.append(row)
            dFX.prNext(fxCntr / listLen)
        dFX.prFin()

    # end getBestMatch

    def getCompleteList(self):
        self.exportData = []
        listLen = len(self.tracedPlayers)
        print('Generate complete list ({})'.format(listLen))
        dFX = DisplayFX.DisplayFX(intVal=0.20, defSet=3, sep='%', filler=1)
        for fxCntr, seq in enumerate(sorted(self.tracedPlayers)):
            row = [[seq] + self.sourceData[int(seq)][1:]]
            for memberId in self.tracedPlayers[seq]:
                row.append(memberId)
            self.exportData.append(row)
            dFX.prNext(fxCntr / listLen)
        dFX.prFin()

    # end getCompleteList

    def indexData(self, p_SourceData, p_SourceDataHeader):
        if not self.silent:
            print('Index data...')
        self.sourceData = p_SourceData.copy()
        self.sourceDataHeader = ['Index'] + p_SourceDataHeader.copy()
        self.surnameSearchedDataIdx = self.sourceDataHeader.index('Surname')
        self.nameSearchedDataIdx = self.sourceDataHeader.index('Name')
        for i in range(len(self.sourceData)):
            self.sourceData[i] = [i] + self.sourceData[i]
        if not self.memberDataIndexed:
            # self.memberDataHeader = ['Index']+ ['Seq']+ self.memberDataHeader
            # self.surnameMemberDataIdx = self.memberDataHeader.index('Surname')
            # self.nameMemberDataIdx = self.memberDataHeader.index('Name')
            for i, memberId in enumerate(self.memberData):
                # self.memberData[memberId]['Idx']= ''
                self.memberData[memberId]['Seq'] = i
            self.memberDataIndexed = True
        if 'Init' in self.memberDataHeader:
            self.initMemberDataIdx = self.memberDataHeader.index('Init')
        if 'DOB' in self.sourceDataHeader:
            self.dOBSearchedDataIdx = self.sourceDataHeader.index('DOB')
        if 'Year' in self.sourceDataHeader:
            self.yearSearchedDataIdx = self.sourceDataHeader.index('Year')

    # end indexData

    def lookUp(self, p_Source, p_DestField, p_SourceUnique=False):
        result = None
        if 'MemberId' in p_Source or p_SourceUnique:
            for key in p_Source:
                if p_Source[key] in self.memberData:
                    result = self.memberData[p_Source[key]][p_DestField]
                else:
                    result = ''
        else:
            result = []
            for memberId in self.memberData:
                for key in p_Source:
                    if self.memberData[memberId][key] == p_Source[key]:
                        result.append(self.memberData[memberId][p_DestField])
        return result

    # def lookUp

    def validateMemberId(self, p_MemberDetail):
        surnameExist = False
        nameExist = False
        dobExist = False
        if 'Surname' in self.memberDataHeader:
            surnameExist = True
        if 'Name' in self.memberDataHeader:
            nameExist = True
        if 'DOB' in self.memberDataHeader:
            dobExist = True
        foundId = False
        if 'MemberId' in p_MemberDetail:
            if p_MemberDetail['MemberId'] in self.memberData:
                foundId = True
                if 'Surname' in p_MemberDetail and surnameExist:
                    if (
                        p_MemberDetail['Surname'].lower()
                        == self.memberData[p_MemberDetail['MemberId']][
                            'Surname'
                        ].lower()
                    ):
                        if 'Name' in p_MemberDetail and nameExist:
                            if (
                                p_MemberDetail['Name'].lower()
                                == self.memberData[p_MemberDetail['MemberId']][
                                    'Name'
                                ].lower()
                            ):
                                if 'DOB' in p_MemberDetail and dobExist:
                                    if (
                                        FixDate.FixDate(
                                            p_MemberDetail['DOB'], dateFormat='%Y/%m/%d'
                                        ).dateStr
                                        != FixDate.FixDate(
                                            self.memberData[p_MemberDetail['MemberId']][
                                                'DOB'
                                            ],
                                            dateFormat='%Y/%m/%d',
                                        ).dateStr
                                    ):
                                        foundId = False
                            else:
                                foundId = False
                    else:
                        foundId = False
        return foundId

    # end validateMemberId


# end PlayerTracer


def ver():
    # ====================================================================
    # Definition: SMWrpr.isPlayerPairingTextFile
    # Created:        18/05/12
    # Description
    #    -
    # Parameters
    #    -
    #    -
    # ====================================================================
    # Change Description
    # --------------------------------------------------------------------
    # -
    #     Name:     Hendrik du Toit
    #     eMail:    hendrik@brightedge.co.za
    #     Date:
    # ====================================================================
    return g_Version


# end ver


def testModule(baseFolder='', cls=True):
    def basicTest():
        def cleanup():
            if os.path.isfile(completeExportPath):
                os.remove(completeExportPath)
            if os.path.isfile(bestMatchExportPath):
                os.remove(bestMatchExportPath)
            if os.path.isfile(smExportPath):
                os.remove(smExportPath)
            if os.path.isfile(smExportPath):
                os.remove(smExportPath)
            if os.path.isfile(generalExportPath):
                os.remove(generalExportPath)

        # end cleanup

        success = True
        if sys.platform.startswith('win32'):
            chessSAMembersPath = os.path.join(
                'D:\\',
                'Dropbox',
                'Projects',
                'PlayerTracer',
                '0200',
                'TestData',
                'ChessSAMembers.csv',
            )
            ursMembersPath = os.path.join(
                'D:\\',
                'Dropbox',
                'Projects',
                'PlayerTracer',
                '0200',
                'TestData',
                'URSMembers.csv',
            )
            completeExportPath = os.path.join(
                'D:\\',
                'Dropbox',
                'Projects',
                'PlayerTracer',
                '0200',
                'TestData',
                'CompleteExport.csv',
            )
            bestMatchExportPath = os.path.join(
                'D:\\',
                'Dropbox',
                'Projects',
                'PlayerTracer',
                '0200',
                'TestData',
                'BestMatchExport.csv',
            )
            smExportPath = os.path.join(
                'D:\\',
                'Dropbox',
                'Projects',
                'PlayerTracer',
                '0200',
                'TestData',
                'SMExport.csv',
            )
            generalExportPath = os.path.join(
                'D:\\',
                'Dropbox',
                'Projects',
                'PlayerTracer',
                '0200',
                'TestData',
                'GeneralExport.csv',
            )
        elif sys.platform.startswith('linux'):
            chessSAMembersPath = os.path.join(
                '/home',
                'hdutoit',
                'Projects',
                'PlayerTracer',
                '0100',
                'TestData',
                'ChessSAMembers.csv',
            )
            completeExportPath = os.path.join(
                '/home',
                'hdutoit',
                'Projects',
                'PlayerTracer',
                '0100',
                'TestData',
                'CompleteExport.csv',
            )
            bestMatchExportPath = os.path.join(
                '/home',
                'hdutoit',
                'Projects',
                'PlayerTracer',
                '0100',
                'TestData',
                'BestMatchExport.csv',
            )
            smExportPath = os.path.join(
                '/home',
                'hdutoit',
                'Projects',
                'PlayerTracer',
                '0100',
                'TestData',
                'SMExport.csv',
            )
        lookUpResult = [
            '168008202',
            '168008203',
            '168008204',
            '268008205',
            '106060686',
            '106060687',
        ]
        # sourceHeader1 = [
        #     'Surname',
        #     'Init',
        #     'Name',
        #     'DOB',
        #     'Region',
        #     'MemberId',
        #     'Standard',
        #     'Gender',
        #     'Title',
        #     'Rapid',
        #     'Blitz',
        # ]
        sourceHeader2 = ['MemberId', 'SurnameName', 'DOB', 'Paid']
        # searchedData1Header = ['Surname', 'Name']
        searchedData2Header = ['Surname', 'Name', 'DOB']
        # searchedData3Header = ['Surname', 'Name', 'DOB', 'ChessSAID']
        searchedData4Header = [
            'No',
            'SurnameName',
            'Title',
            'ID no',
            'Rating nat',
            'Rating int',
            'DOB',
            'Fed',
            'Sex',
            'Type',
            'Gr',
            'Clubno',
            'Club',
            'FIDE-No',
            'Source',
            'pts',
            'tb1',
            'tb2',
            'tb3',
            'tb4',
            'tb5',
            'rank',
            'Surname',
            'Name',
            'atitle',
        ]
        searchedData5Header = ['Surname', 'Name', 'Init', 'DOB', 'Paid']
        # sourceDataExportHeader1 = [
        #     'Surname',
        #     'Name',
        #     'DOB',
        #     'MemberId',
        #     'Gender',
        #     'Region',
        # ]
        # sourceDataExportHeader2 = ['Surname', 'Name', 'DOB', 'PID', 'CID']
        # searchedData1 = [['Du Toit', 'Hendrik'], ['Bierman', 'C']]
        searchedData2 = [
            ['Du Toit', 'Hendrik', '1968/10/20'],
            ['Bierman', 'C', '10/06/01'],
            ['Greef', 'Janus', '06/08/31'],
            ['Greef', 'Schalk', '06/08/31'],
        ]
        # searchedData3 = [
        #     ['Du Toit', 'Hendrik', '1968/10/20', '168008202'],
        #     ['Bierman', 'C', '10/06/01', ''],
        # ]
        searchedData4 = [
            [
                'No',
                'SurnameName',
                'Title',
                'ID no',
                'Rating nat',
                'Rating int',
                'DOB',
                'Fed',
                'Sex',
                'Type',
                'Gr',
                'Clubno',
                'Club',
                'FIDE-No',
                'Source',
                'pts',
                'tb1',
                'tb2',
                'tb3',
                'tb4',
                'tb5',
                'rank',
                'Surname',
                'Name',
                'atitle',
            ],
            [
                '1',
                'Du Toit Hendrik',
                '',
                '168008202',
                '',
                '',
                '1968/10/20',
                'RSA',
                '',
                'Paid',
                'U20',
                '1',
                'Waterkloof',
                '14306980',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Du Toit',
                'Hendrik',
                '',
            ],
            [
                '13',
                'Bierman C',
                '',
                '',
                '',
                '',
                '10/06/01',
                'RSA',
                '',
                'Paid',
                'U18',
                '1',
                'Wierdapark',
                '1110001',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Bierman',
                'C',
                '',
            ],
            [
                '1',
                'Du Toit Hendrik',
                '',
                '168008202',
                '',
                '',
                '1968/10/20',
                'RSA',
                '',
                'Paid',
                'U20',
                '1',
                'Waterkloof',
                '14306980',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Du Toit',
                'Hendrik',
                '',
            ],
            [
                '14',
                'Other Ann',
                '',
                '',
                '',
                '',
                '2005/05/31',
                'RSA',
                '',
                'Paid',
                'U16',
                '1',
                'Waterkloof',
                '',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Other',
                'Ann',
                '',
            ],
            [
                '15',
                'Blogs Joe',
                '',
                '',
                '',
                '',
                '2007/07/31',
                'RSA',
                '',
                'Paid',
                'U18',
                '1',
                'Waterkloof',
                '',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Blogs',
                'Joe',
                '',
            ],
        ]
        searchedData5 = [
            ['Surname', 'Name', 'Init', 'DOB', 'Paid'],
            ['Du Toit', 'Hendrik', 'HP', '1968/10/20', 'Yes'],
            ['Steenkamp', 'Ruan', 'R', '90/04/06', 'No'],
        ]
        # testDataRaw1 = {
        #     '100000199': {
        #         'Seq': 0,
        #         'Surname': 'ADAMS',
        #         'Init': 'G',
        #         'Name': 'GRANT',
        #         'DOB': '01/01/01',
        #         'Region': 'WP',
        #         'MemberId': '100000199',
        #         'Standard': '1063',
        #         'Gender': 'M',
        #         'Title': '',
        #         'Rapid': '1053',
        #         'Blitz': '1053',
        #     },
        #     '168008202': {
        #         'Seq': 1,
        #         'Surname': 'DU TOIT',
        #         'Init': 'HP',
        #         'Name': 'HENDRIK',
        #         'DOB': '1968/10/20',
        #         'Region': 'GTP',
        #         'MemberId': '168008202',
        #         'Standard': '1161',
        #         'Gender': 'M',
        #         'Title': 'IA',
        #         'Rapid': '1185',
        #         'Blitz': '1185',
        #         'Priority': 3,
        #     },
        #     '168008203': {
        #         'Seq': 2,
        #         'Surname': 'DU TOIT',
        #         'Init': 'HP',
        #         'Name': 'HENDRIK',
        #         'DOB': '66/10/20',
        #         'Region': 'GTP',
        #         'MemberId': '168008203',
        #         'Standard': '1161',
        #         'Gender': 'M',
        #         'Title': 'IA',
        #         'Rapid': '1185',
        #         'Blitz': '1185',
        #         'Priority': 3,
        #     },
        #     '168008204': {
        #         'Seq': 3,
        #         'Surname': 'DU TOIT',
        #         'Init': 'H',
        #         'Name': 'H',
        #         'DOB': '1966/10/20',
        #         'Region': 'GTP',
        #         'MemberId': '168008204',
        #         'Standard': '1161',
        #         'Gender': 'M',
        #         'Title': 'IA',
        #         'Rapid': '1185',
        #         'Blitz': '1185',
        #         'Priority': 4,
        #     },
        #     '187000287': {
        #         'Seq': 4,
        #         'Surname': 'ADLY',
        #         'Init': 'A',
        #         'Name': 'AHMED',
        #         'DOB': '87/01/01',
        #         'Region': 'UNK',
        #         'MemberId': '187000287',
        #         'Standard': '2598',
        #         'Gender': 'M',
        #         'Title': '',
        #         'Rapid': '2598',
        #         'Blitz': '2598',
        #     },
        #     '268008205': {
        #         'Seq': 5,
        #         'Surname': 'DU TOIT',
        #         'Init': 'HP',
        #         'Name': 'HENDRIK',
        #         'DOB': '68/10/20',
        #         'Region': 'GTP',
        #         'MemberId': '268008205',
        #         'Standard': '1161',
        #         'Gender': 'F',
        #         'Title': 'IA',
        #         'Rapid': '1185',
        #         'Blitz': '1185',
        #         'Priority': 3,
        #     },
        #     '110089038': {
        #         'Seq': 6,
        #         'Surname': 'BIERMAN',
        #         'Init': 'C',
        #         'Name': 'CORNELIUS',
        #         'DOB': '10/06/01',
        #         'Region': 'MGS',
        #         'MemberId': '110089038',
        #         'Standard': '563',
        #         'Gender': 'M',
        #         'Title': '',
        #         'Rapid': '500',
        #         'Blitz': '500',
        #         'Priority': 4,
        #     },
        #     '110089039': {
        #         'Seq': 7,
        #         'Surname': 'BIERMAN',
        #         'Init': 'C',
        #         'Name': 'C',
        #         'DOB': '2010/06/01',
        #         'Region': 'MGS',
        #         'MemberId': '110089039',
        #         'Standard': '563',
        #         'Gender': 'M',
        #         'Title': '',
        #         'Rapid': '500',
        #         'Blitz': '500',
        #         'Priority': 3,
        #     },
        #     '106060686': {
        #         'Seq': 8,
        #         'Surname': 'Greef',
        #         'Init': 'J',
        #         'Name': 'Janus Dirk',
        #         'DOB': '06/08/31',
        #         'Region': 'GTP',
        #         'MemberId': '106060686',
        #         'Standard': '0',
        #         'Gender': 'M',
        #         'Title': '',
        #         'Rapid': '0',
        #         'Blitz': '0',
        #     },
        #     '106060687': {
        #         'Seq': 9,
        #         'Surname': 'Greef',
        #         'Init': 'S',
        #         'Name': 'Schalk Gerhardus',
        #         'DOB': '06/08/31',
        #         'Region': 'GTP',
        #         'MemberId': '106060687',
        #         'Standard': '0',
        #         'Gender': 'M',
        #         'Title': '',
        #         'Rapid': '0',
        #         'Blitz': '0',
        #     },
        # }
        testDataRaw2 = {
            '100000199': {
                'Surname': 'ADAMS',
                'Init': 'G',
                'Name': 'GRANT',
                'DOB': '01/01/01',
                'Region': 'WP',
                'MemberId': '100000199',
                'Standard': '1063',
                'Gender': 'M',
                'Title': '',
                'Rapid': '1053',
                'Blitz': '1053',
                'Seq': 0,
            },
            '168008202': {
                'Surname': 'DU TOIT',
                'Init': 'HP',
                'Name': 'HENDRIK',
                'DOB': '1968/10/20',
                'Region': 'GTP',
                'MemberId': '168008202',
                'Standard': '1161',
                'Gender': 'M',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 1,
                'Priority': 0,
            },
            '168008203': {
                'Surname': 'DU TOIT',
                'Init': 'HP',
                'Name': 'HENDRIK',
                'DOB': '66/10/20',
                'Region': 'GTP',
                'MemberId': '168008203',
                'Standard': '1161',
                'Gender': 'M',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 2,
                'Priority': 3,
            },
            '168008204': {
                'Surname': 'DU TOIT',
                'Init': 'H',
                'Name': 'H',
                'DOB': '1966/10/20',
                'Region': 'GTP',
                'MemberId': '168008204',
                'Standard': '1161',
                'Gender': 'M',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 3,
                'Priority': 4,
            },
            '187000287': {
                'Surname': 'ADLY',
                'Init': 'A',
                'Name': 'AHMED',
                'DOB': '87/01/01',
                'Region': 'UNK',
                'MemberId': '187000287',
                'Standard': '2598',
                'Gender': 'M',
                'Title': '',
                'Rapid': '2598',
                'Blitz': '2598',
                'Seq': 4,
            },
            '268008205': {
                'Surname': 'DU TOIT',
                'Init': 'HP',
                'Name': 'HENDRIK',
                'DOB': '68/10/20',
                'Region': 'GTP',
                'MemberId': '268008205',
                'Standard': '1161',
                'Gender': 'F',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 5,
                'Priority': 0,
            },
            '110089038': {
                'Surname': 'BIERMAN',
                'Init': 'C',
                'Name': 'CORNELIUS',
                'DOB': '10/06/01',
                'Region': 'MGS',
                'MemberId': '110089038',
                'Standard': '563',
                'Gender': 'M',
                'Title': '',
                'Rapid': '500',
                'Blitz': '500',
                'Seq': 6,
                'Priority': 1,
            },
            '110089039': {
                'Surname': 'BIERMAN',
                'Init': 'C',
                'Name': 'C',
                'DOB': '2010/06/01',
                'Region': 'MGS',
                'MemberId': '110089039',
                'Standard': '563',
                'Gender': 'M',
                'Title': '',
                'Rapid': '500',
                'Blitz': '500',
                'Seq': 7,
                'Priority': 0,
            },
            '106060686': {
                'Surname': 'Greef',
                'Init': 'J',
                'Name': 'Janus Dirk',
                'DOB': '06/08/31',
                'Region': 'GTP',
                'MemberId': '106060686',
                'Standard': '0',
                'Gender': 'M',
                'Title': '',
                'Rapid': '0',
                'Blitz': '0',
                'Seq': 8,
                'Priority': 2,
            },
            '106060687': {
                'Surname': 'Greef',
                'Init': 'S',
                'Name': 'Schalk Gerhardus',
                'DOB': '06/08/31',
                'Region': 'GTP',
                'MemberId': '106060687',
                'Standard': '0',
                'Gender': 'M',
                'Title': '',
                'Rapid': '0',
                'Blitz': '0',
                'Seq': 9,
                'Priority': 1,
            },
        }
        testDataRaw3 = {
            '100000199': {
                'Surname': 'ADAMS',
                'Init': 'G',
                'Name': 'GRANT',
                'DOB': '01/01/01',
                'Region': 'WP',
                'MemberId': '100000199',
                'Standard': '1063',
                'Gender': 'M',
                'Title': '',
                'Rapid': '1053',
                'Blitz': '1053',
                'Seq': 0,
            },
            '168008202': {
                'Surname': 'DU TOIT',
                'Init': 'HP',
                'Name': 'HENDRIK',
                'DOB': '1968/10/20',
                'Region': 'GTP',
                'MemberId': '168008202',
                'Standard': '1161',
                'Gender': 'M',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 1,
                'Priority': 0,
            },
            '168008203': {
                'Surname': 'DU TOIT',
                'Init': 'HP',
                'Name': 'HENDRIK',
                'DOB': '66/10/20',
                'Region': 'GTP',
                'MemberId': '168008203',
                'Standard': '1161',
                'Gender': 'M',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 2,
                'Priority': 3,
            },
            '168008204': {
                'Surname': 'DU TOIT',
                'Init': 'H',
                'Name': 'H',
                'DOB': '1966/10/20',
                'Region': 'GTP',
                'MemberId': '168008204',
                'Standard': '1161',
                'Gender': 'M',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 3,
                'Priority': 4,
            },
            '187000287': {
                'Surname': 'ADLY',
                'Init': 'A',
                'Name': 'AHMED',
                'DOB': '87/01/01',
                'Region': 'UNK',
                'MemberId': '187000287',
                'Standard': '2598',
                'Gender': 'M',
                'Title': '',
                'Rapid': '2598',
                'Blitz': '2598',
                'Seq': 4,
            },
            '268008205': {
                'Surname': 'DU TOIT',
                'Init': 'HP',
                'Name': 'HENDRIK',
                'DOB': '68/10/20',
                'Region': 'GTP',
                'MemberId': '268008205',
                'Standard': '1161',
                'Gender': 'F',
                'Title': 'IA',
                'Rapid': '1185',
                'Blitz': '1185',
                'Seq': 5,
                'Priority': 0,
            },
            '110089038': {
                'Surname': 'BIERMAN',
                'Init': 'C',
                'Name': 'CORNELIUS',
                'DOB': '10/06/01',
                'Region': 'MGS',
                'MemberId': '110089038',
                'Standard': '563',
                'Gender': 'M',
                'Title': '',
                'Rapid': '500',
                'Blitz': '500',
                'Seq': 6,
                'Priority': 1,
            },
            '110089039': {
                'Surname': 'BIERMAN',
                'Init': 'C',
                'Name': 'C',
                'DOB': '2010/06/01',
                'Region': 'MGS',
                'MemberId': '110089039',
                'Standard': '563',
                'Gender': 'M',
                'Title': '',
                'Rapid': '500',
                'Blitz': '500',
                'Seq': 7,
                'Priority': 0,
            },
            '106060686': {
                'Surname': 'Greef',
                'Init': 'J',
                'Name': 'Janus Dirk',
                'DOB': '06/08/31',
                'Region': 'GTP',
                'MemberId': '106060686',
                'Standard': '0',
                'Gender': 'M',
                'Title': '',
                'Rapid': '0',
                'Blitz': '0',
                'Seq': 8,
            },
            '106060687': {
                'Surname': 'Greef',
                'Init': 'S',
                'Name': 'Schalk Gerhardus',
                'DOB': '06/08/31',
                'Region': 'GTP',
                'MemberId': '106060687',
                'Standard': '0',
                'Gender': 'M',
                'Title': '',
                'Rapid': '0',
                'Blitz': '0',
                'Seq': 9,
            },
        }
        testDataRaw4 = {
            '1': {
                'MemberId': '1',
                'SurnameName': 'Surname1,Name1',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname1',
                'Name': 'Name1',
                'Seq': 0,
            },
            '2': {
                'MemberId': '2',
                'SurnameName': 'Surname2,Name2',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname2',
                'Name': 'Name2',
                'Seq': 1,
            },
            '3': {
                'MemberId': '3',
                'SurnameName': 'Surname3,Name3',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname3',
                'Name': 'Name3',
                'Seq': 2,
            },
            '4': {
                'MemberId': '4',
                'SurnameName': 'Surname4,Name4',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname4',
                'Name': 'Name4',
                'Seq': 3,
            },
            '5': {
                'MemberId': '5',
                'SurnameName': 'Du Toit,Hendrik',
                'DOB': '68/10/20',
                'Paid': 'Yes',
                'Surname': 'Du Toit',
                'Name': 'Hendrik',
                'Seq': 4,
                'Priority': 0,
            },
            '6': {
                'MemberId': '6',
                'SurnameName': 'Surname6,Name6',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname6',
                'Name': 'Name6',
                'Seq': 5,
            },
            '7': {
                'MemberId': '7',
                'SurnameName': 'Surname7,Name7',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname7',
                'Name': 'Name7',
                'Seq': 6,
            },
            '8': {
                'MemberId': '8',
                'SurnameName': 'Steenkamp,Ruan',
                'DOB': '90/04/06',
                'Paid': 'No',
                'Surname': 'Steenkamp',
                'Name': 'Ruan',
                'Seq': 7,
                'Priority': 0,
            },
            '9': {
                'MemberId': '9',
                'SurnameName': 'Surname9,Name9',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname9',
                'Name': 'Name9',
                'Seq': 8,
            },
            '10': {
                'MemberId': '10',
                'SurnameName': 'Surname10,Name10',
                'DOB': '90/01/01',
                'Paid': 'Yes',
                'Surname': 'Surname10',
                'Name': 'Name10',
                'Seq': 9,
            },
        }
        # testDataCompleteExport1 = [
        #     [
        #         [0, 'Du Toit', 'Hendrik'],
        #         '168008202',
        #         '168008203',
        #         '268008205',
        #         '168008204',
        #     ],
        #     [[1, 'Bierman', 'C'], '110089039', '110089038'],
        # ]
        # testDataCompleteExport2 = [
        #     ['0', 'Du Toit', 'Hendrik'],
        #     [
        #         'DU TOIT',
        #         'HP',
        #         'HENDRIK',
        #         '1968/10/20',
        #         'GTP',
        #         '168008202',
        #         '1161',
        #         'M',
        #         'IA',
        #         '1185',
        #         '1185',
        #         '1',
        #         '3',
        #     ],
        #     [
        #         'DU TOIT',
        #         'HP',
        #         'HENDRIK',
        #         '66/10/20',
        #         'GTP',
        #         '168008203',
        #         '1161',
        #         'M',
        #         'IA',
        #         '1185',
        #         '1185',
        #         '2',
        #         '3',
        #     ],
        #     [
        #         'DU TOIT',
        #         'HP',
        #         'HENDRIK',
        #         '68/10/20',
        #         'GTP',
        #         '268008205',
        #         '1161',
        #         'F',
        #         'IA',
        #         '1185',
        #         '1185',
        #         '5',
        #         '3',
        #     ],
        #     [
        #         'DU TOIT',
        #         'H',
        #         'H',
        #         '1966/10/20',
        #         'GTP',
        #         '168008204',
        #         '1161',
        #         'M',
        #         'IA',
        #         '1185',
        #         '1185',
        #         '3',
        #         '4',
        #     ],
        #     [''],
        #     ['1', 'Bierman', 'C'],
        #     [
        #         'BIERMAN',
        #         'C',
        #         'C',
        #         '2010/06/01',
        #         'MGS',
        #         '110089039',
        #         '563',
        #         'M',
        #         '',
        #         '500',
        #         '500',
        #         '7',
        #         '3',
        #     ],
        #     [
        #         'BIERMAN',
        #         'C',
        #         'CORNELIUS',
        #         '10/06/01',
        #         'MGS',
        #         '110089038',
        #         '563',
        #         'M',
        #         '',
        #         '500',
        #         '500',
        #         '6',
        #         '4',
        #     ],
        #     [''],
        # ]
        testDataCompleteExport3 = [
            [
                [0, 'Du Toit', 'Hendrik', '1968/10/20'],
                '168008202',
                '268008205',
                '168008203',
                '168008204',
            ],
            [[1, 'Bierman', 'C', '10/06/01'], '110089039', '110089038'],
            [[2, 'Greef', 'Janus', '06/08/31'], '106060686', '106060687'],
            [[3, 'Greef', 'Schalk', '06/08/31'], '106060687', '106060686'],
        ]
        testDataCompleteExport4 = [
            ['0', 'Du Toit', 'Hendrik', '1968/10/20'],
            [
                'DU TOIT',
                'HP',
                'HENDRIK',
                '1968/10/20',
                'GTP',
                '168008202',
                '1161',
                'M',
                'IA',
                '1185',
                '1185',
                '1',
                '0',
            ],
            [
                'DU TOIT',
                'HP',
                'HENDRIK',
                '68/10/20',
                'GTP',
                '268008205',
                '1161',
                'F',
                'IA',
                '1185',
                '1185',
                '5',
                '0',
            ],
            [
                'DU TOIT',
                'HP',
                'HENDRIK',
                '66/10/20',
                'GTP',
                '168008203',
                '1161',
                'M',
                'IA',
                '1185',
                '1185',
                '2',
                '3',
            ],
            [
                'DU TOIT',
                'H',
                'H',
                '1966/10/20',
                'GTP',
                '168008204',
                '1161',
                'M',
                'IA',
                '1185',
                '1185',
                '3',
                '4',
            ],
            [''],
            ['1', 'Bierman', 'C', '10/06/01'],
            [
                'BIERMAN',
                'C',
                'C',
                '2010/06/01',
                'MGS',
                '110089039',
                '563',
                'M',
                '',
                '500',
                '500',
                '7',
                '0',
            ],
            [
                'BIERMAN',
                'C',
                'CORNELIUS',
                '10/06/01',
                'MGS',
                '110089038',
                '563',
                'M',
                '',
                '500',
                '500',
                '6',
                '1',
            ],
            [''],
            ['2', 'Greef', 'Janus', '06/08/31'],
            [
                'Greef',
                'J',
                'Janus Dirk',
                '06/08/31',
                'GTP',
                '106060686',
                '0',
                'M',
                '',
                '0',
                '0',
                '8',
                '2',
            ],
            [
                'Greef',
                'S',
                'Schalk Gerhardus',
                '06/08/31',
                'GTP',
                '106060687',
                '0',
                'M',
                '',
                '0',
                '0',
                '9',
                '1',
            ],
            [''],
            ['3', 'Greef', 'Schalk', '06/08/31'],
            [
                'Greef',
                'S',
                'Schalk Gerhardus',
                '06/08/31',
                'GTP',
                '106060687',
                '0',
                'M',
                '',
                '0',
                '0',
                '9',
                '1',
            ],
            [
                'Greef',
                'J',
                'Janus Dirk',
                '06/08/31',
                'GTP',
                '106060686',
                '0',
                'M',
                '',
                '0',
                '0',
                '8',
                '2',
            ],
            [''],
        ]
        # testDataBestMatchExport1 = [
        #     [[0, 'Du Toit', 'Hendrik'], '168008202'],
        #     [[1, 'Bierman', 'C'], '110089039'],
        # ]
        # testDataBestMatchExport2 = [
        #     ['0', 'Du Toit', 'Hendrik'],
        #     [
        #         'DU TOIT',
        #         'HP',
        #         'HENDRIK',
        #         '1968/10/20',
        #         'GTP',
        #         '168008202',
        #         '1161',
        #         'M',
        #         'IA',
        #         '1185',
        #         '1185',
        #         '1',
        #         '3',
        #     ],
        #     [''],
        #     ['1', 'Bierman', 'C'],
        #     [
        #         'BIERMAN',
        #         'C',
        #         'C',
        #         '2010/06/01',
        #         'MGS',
        #         '110089039',
        #         '563',
        #         'M',
        #         '',
        #         '500',
        #         '500',
        #         '7',
        #         '3',
        #     ],
        #     [''],
        # ]
        testDataBestMatchExport3 = [
            [[0, 'Du Toit', 'Hendrik', '1968/10/20'], '168008202'],
            [[1, 'Bierman', 'C', '10/06/01'], '110089039'],
            [[2, 'Greef', 'Janus', '06/08/31'], '106060686'],
            [[3, 'Greef', 'Schalk', '06/08/31'], '106060687'],
        ]
        testDataBestMatchExport4 = [
            ['0', 'Du Toit', 'Hendrik', '1968/10/20'],
            [
                'DU TOIT',
                'HP',
                'HENDRIK',
                '1968/10/20',
                'GTP',
                '168008202',
                '1161',
                'M',
                'IA',
                '1185',
                '1185',
                '1',
                '0',
            ],
            [''],
            ['1', 'Bierman', 'C', '10/06/01'],
            [
                'BIERMAN',
                'C',
                'C',
                '2010/06/01',
                'MGS',
                '110089039',
                '563',
                'M',
                '',
                '500',
                '500',
                '7',
                '0',
            ],
            [''],
            ['2', 'Greef', 'Janus', '06/08/31'],
            [
                'Greef',
                'J',
                'Janus Dirk',
                '06/08/31',
                'GTP',
                '106060686',
                '0',
                'M',
                '',
                '0',
                '0',
                '8',
                '2',
            ],
            [''],
            ['3', 'Greef', 'Schalk', '06/08/31'],
            [
                'Greef',
                'S',
                'Schalk Gerhardus',
                '06/08/31',
                'GTP',
                '106060687',
                '0',
                'M',
                '',
                '0',
                '0',
                '9',
                '1',
            ],
            [''],
        ]
        testDataBestMatchExport5 = [
            [[0, 'Surname', 'Name', 'Init', 'DOB', 'Paid']],
            [[1, 'Du Toit', 'Hendrik', 'HP', '1968/10/20', 'Yes'], '5'],
            [[2, 'Steenkamp', 'Ruan', 'R', '90/04/06', 'No'], '8'],
        ]
        testDataSMExport1 = [
            [
                [
                    0,
                    'No',
                    'SurnameName',
                    'Title',
                    'ID no',
                    'Rating nat',
                    'Rating int',
                    'DOB',
                    'Fed',
                    'Sex',
                    'Type',
                    'Gr',
                    'Clubno',
                    'Club',
                    'FIDE-No',
                    'Source',
                    'pts',
                    'tb1',
                    'tb2',
                    'tb3',
                    'tb4',
                    'tb5',
                    'rank',
                    'Surname',
                    'Name',
                    'atitle',
                ]
            ],
            [
                [
                    1,
                    '1',
                    'Du Toit Hendrik',
                    '',
                    '168008202',
                    '',
                    '',
                    '1968/10/20',
                    'RSA',
                    '',
                    'Paid',
                    'U20',
                    '1',
                    'Waterkloof',
                    '14306980',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Du Toit',
                    'Hendrik',
                    '',
                ],
                '168008202',
            ],
            [
                [
                    2,
                    '13',
                    'Bierman C',
                    '',
                    '110089039',
                    '',
                    '',
                    '10/06/01',
                    'RSA',
                    '',
                    'Paid',
                    'U18',
                    '1',
                    'Wierdapark',
                    '1110001',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Bierman',
                    'C',
                    '',
                ],
                '110089039',
            ],
            [
                [
                    3,
                    '1',
                    'Du Toit Hendrik',
                    '',
                    '168008202',
                    '',
                    '',
                    '1968/10/20',
                    'RSA',
                    '',
                    'Paid',
                    'U20',
                    '1',
                    'Waterkloof',
                    '14306980',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Du Toit',
                    'Hendrik',
                    '',
                ],
                '168008202',
            ],
            [
                [
                    4,
                    '14',
                    'Other Ann',
                    '',
                    '',
                    '',
                    '',
                    '2005/05/31',
                    'RSA',
                    '',
                    'Paid',
                    'U16',
                    '1',
                    'Waterkloof',
                    '',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Other',
                    'Ann',
                    '',
                ]
            ],
            [
                [
                    5,
                    '15',
                    'Blogs Joe',
                    '',
                    '',
                    '',
                    '',
                    '2007/07/31',
                    'RSA',
                    '',
                    'Paid',
                    'U18',
                    '1',
                    'Waterkloof',
                    '',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Blogs',
                    'Joe',
                    '',
                ]
            ],
        ]
        testDataSMExport2 = [
            [
                'No',
                'SurnameName',
                'Title',
                'ID no',
                'Rating nat',
                'Rating int',
                'DOB',
                'Fed',
                'Sex',
                'Type',
                'Gr',
                'Clubno',
                'Club',
                'FIDE-No',
                'Source',
                'pts',
                'tb1',
                'tb2',
                'tb3',
                'tb4',
                'tb5',
                'rank',
                'Surname',
                'Name',
                'atitle',
            ],
            # ['1', 'Du Toit Hendrik', '', '168008202', '1161', '', '1968/10/20', 'RSA', '', 'Paid', 'U20', '1', 'Waterkloof', '14306980', 'RSA', '0', '0', '0', '0', '0', '0', '', 'Du Toit', 'Hendrik', ''],
            [
                '1',
                'Du Toit Hendrik',
                '',
                '168008202',
                '',
                '',
                '1968/10/20',
                'RSA',
                '',
                'Paid',
                'U20',
                '1',
                'Waterkloof',
                '14306980',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Du Toit',
                'Hendrik',
                '',
            ],
            # ['13', 'Bierman C', '', '110089039', '563', '', '10/06/01', 'RSA', '', 'Paid', 'U18', '1', 'Wierdapark', '1110001', 'RSA', '0', '0', '0', '0', '0', '0', '', 'Bierman', 'C', ''],
            [
                '13',
                'Bierman C',
                '',
                '110089039',
                '',
                '',
                '10/06/01',
                'RSA',
                '',
                'Paid',
                'U18',
                '1',
                'Wierdapark',
                '1110001',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Bierman',
                'C',
                '',
            ],
            [
                '14',
                'Other Ann',
                '',
                '',
                '',
                '',
                '2005/05/31',
                'RSA',
                '',
                'Paid',
                'U16',
                '1',
                'Waterkloof',
                '',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Other',
                'Ann',
                '',
            ],
            [
                '15',
                'Blogs Joe',
                '',
                '',
                '',
                '',
                '2007/07/31',
                'RSA',
                '',
                'Paid',
                'U18',
                '1',
                'Waterkloof',
                '',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Blogs',
                'Joe',
                '',
            ],
        ]
        testDataSMExport3 = [
            [
                [
                    0,
                    'No',
                    'SurnameName',
                    'Title',
                    'ID no',
                    'Rating nat',
                    'Rating int',
                    'DOB',
                    'Fed',
                    'Sex',
                    'Type',
                    'Gr',
                    'Clubno',
                    'Club',
                    'FIDE-No',
                    'Source',
                    'pts',
                    'tb1',
                    'tb2',
                    'tb3',
                    'tb4',
                    'tb5',
                    'rank',
                    'Surname',
                    'Name',
                    'atitle',
                ]
            ],
            [
                [
                    1,
                    '1',
                    'Du Toit Hendrik',
                    '',
                    '168008202',
                    '1161',
                    '',
                    '1968/10/20',
                    'RSA',
                    '',
                    'Paid',
                    'U20',
                    '1',
                    'Waterkloof',
                    '14306980',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Du Toit',
                    'Hendrik',
                    '',
                ],
                '168008202',
            ],
            [
                [
                    2,
                    '13',
                    'Bierman C',
                    '',
                    '110089039',
                    '563',
                    '',
                    '10/06/01',
                    'RSA',
                    '',
                    'Paid',
                    'U18',
                    '1',
                    'Wierdapark',
                    '1110001',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Bierman',
                    'C',
                    '',
                ],
                '110089039',
            ],
            [
                [
                    3,
                    '1',
                    'Du Toit Hendrik',
                    '',
                    '168008202',
                    '1161',
                    '',
                    '1968/10/20',
                    'RSA',
                    '',
                    'Paid',
                    'U20',
                    '1',
                    'Waterkloof',
                    '14306980',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Du Toit',
                    'Hendrik',
                    '',
                ],
                '168008202',
            ],
            [
                [
                    4,
                    '14',
                    'Other Ann',
                    '',
                    '',
                    '',
                    '',
                    '2005/05/31',
                    'RSA',
                    '',
                    'Paid',
                    'U16',
                    '1',
                    'Waterkloof',
                    '',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Other',
                    'Ann',
                    '',
                ]
            ],
            [
                [
                    5,
                    '15',
                    'Blogs Joe',
                    '',
                    '',
                    '',
                    '',
                    '2007/07/31',
                    'RSA',
                    '',
                    'Paid',
                    'U18',
                    '1',
                    'Waterkloof',
                    '',
                    'RSA',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '0',
                    '',
                    'Blogs',
                    'Joe',
                    '',
                ]
            ],
        ]
        testDataSMExport4 = [
            [
                'No',
                'SurnameName',
                'Title',
                'ID no',
                'Rating nat',
                'Rating int',
                'DOB',
                'Fed',
                'Sex',
                'Type',
                'Gr',
                'Clubno',
                'Club',
                'FIDE-No',
                'Source',
                'pts',
                'tb1',
                'tb2',
                'tb3',
                'tb4',
                'tb5',
                'rank',
                'Surname',
                'Name',
                'atitle',
            ],
            [
                '1',
                'Du Toit Hendrik',
                '',
                '168008202',
                '1161',
                '',
                '1968/10/20',
                'RSA',
                '',
                'Paid',
                'U20',
                '1',
                'Waterkloof',
                '14306980',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Du Toit',
                'Hendrik',
                '',
            ],
            [
                '13',
                'Bierman C',
                '',
                '110089039',
                '563',
                '',
                '10/06/01',
                'RSA',
                '',
                'Paid',
                'U18',
                '1',
                'Wierdapark',
                '1110001',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Bierman',
                'C',
                '',
            ],
            [
                '14',
                'Other Ann',
                '',
                '',
                '',
                '',
                '2005/05/31',
                'RSA',
                '',
                'Paid',
                'U16',
                '1',
                'Waterkloof',
                '',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Other',
                'Ann',
                '',
            ],
            [
                '15',
                'Blogs Joe',
                '',
                '',
                '',
                '',
                '2007/07/31',
                'RSA',
                '',
                'Paid',
                'U18',
                '1',
                'Waterkloof',
                '',
                'RSA',
                '0',
                '0',
                '0',
                '0',
                '0',
                '0',
                '',
                'Blogs',
                'Joe',
                '',
            ],
        ]
        testDataGeneralExport1 = [
            ['0', 'Surname', 'Name', 'Init', 'DOB', 'Paid'],
            [''],
            ['1', 'Du Toit', 'Hendrik', 'HP', '1968/10/20', 'Yes'],
            ['5', 'Du Toit,Hendrik', '68/10/20', 'Yes', 'Du Toit', 'Hendrik', '4', '0'],
            [''],
            ['2', 'Steenkamp', 'Ruan', 'R', '90/04/06', 'No'],
            ['8', 'Steenkamp,Ruan', '90/04/06', 'No', 'Steenkamp', 'Ruan', '7', '0'],
            [''],
        ]
        # testDataCheckIDExport1 = [
        #     [
        #         1,
        #         0,
        #         7,
        #         'BIERMAN',
        #         'C',
        #         'C',
        #         '2010/06/01',
        #         'MGS',
        #         '110089038',
        #         '563',
        #         'M',
        #         '',
        #         '500',
        #         '500',
        #     ],
        #     [
        #         1,
        #         1,
        #         6,
        #         'BIERMAN',
        #         'C',
        #         'CORNELIUS',
        #         '10/06/01',
        #         'MGS',
        #         '110089038',
        #         '563',
        #         'M',
        #         '',
        #         '500',
        #         '500',
        #     ],
        # ]
        # testDataCheckIDExport2 = [
        #     [
        #         '1',
        #         '0',
        #         '7',
        #         'BIERMAN',
        #         'C',
        #         'C',
        #         '2010/06/01',
        #         'MGS',
        #         '110089038',
        #         '563',
        #         'M',
        #         '',
        #         '500',
        #         '500',
        #     ],
        #     [
        #         '1',
        #         '1',
        #         '6',
        #         'BIERMAN',
        #         'C',
        #         'CORNELIUS',
        #         '10/06/01',
        #         'MGS',
        #         '110089038',
        #         '563',
        #         'M',
        #         '',
        #         '500',
        #         '500',
        #     ],
        # ]
        testfindMemberId1 = {'Name': 'Hendrik', 'Surname': 'Du Toit'}
        testfindMemberId2 = {'Name': 'Hendrik', 'Surname': 'Du Toit', 'Year': 1968}

        # cleanup()
        # playerTracer = PlayerTracer(chessSAMembersPath, searchedData1, searchedData1Header)
        # success = rtutils.isStructTheSame(playerTracer.memberData, testDataRaw1) and success
        # playerTracer.getCompleteList()
        # playerTracer.exportToCsv(completeExportPath)
        # success = rtutils.isStructTheSame(playerTracer.exportData, testDataCompleteExport1) and success
        # exportedFileData = CsvWrpr.CsvWrpr(completeExportPath, delHead = 'Do not', strucType = 'List')
        # success = rtutils.isStructTheSame(exportedFileData.csvDb, testDataCompleteExport2) and success
        # playerTracer.getBestMatch()
        # playerTracer.exportToCsv(bestMatchExportPath)
        # success = rtutils.isStructTheSame(playerTracer.exportData, testDataBestMatchExport1) and success
        # exportedFileData = CsvWrpr.CsvWrpr(bestMatchExportPath, delHead = 'Do not', strucType = 'List')
        # success = rtutils.isStructTheSame(exportedFileData.csvDb, testDataBestMatchExport2) and success

        cleanup()
        playerTracer = PlayerTracer(
            chessSAMembersPath, searchedData2, searchedData2Header
        )
        success = (
            rtutils.isStructTheSame(playerTracer.memberData, testDataRaw2) and success
        )
        playerTracer.getCompleteList()
        playerTracer.exportToCsv(completeExportPath)
        success = (
            rtutils.isStructTheSame(playerTracer.exportData, testDataCompleteExport3)
            and success
        )
        exportedFileData = CsvWrpr.CsvWrpr(
            completeExportPath, delHead='Do not', strucType='List'
        )
        success = (
            rtutils.isStructTheSame(exportedFileData.csvDb, testDataCompleteExport4)
            and success
        )
        playerTracer.getBestMatch()
        playerTracer.exportToCsv(bestMatchExportPath)
        success = (
            rtutils.isStructTheSame(playerTracer.exportData, testDataBestMatchExport3)
            and success
        )
        exportedFileData = CsvWrpr.CsvWrpr(
            bestMatchExportPath, delHead='Do not', strucType='List'
        )
        success = (
            rtutils.isStructTheSame(exportedFileData.csvDb, testDataBestMatchExport4)
            and success
        )

        cleanup()
        playerTracer = PlayerTracer(
            chessSAMembersPath, searchedData4, searchedData4Header
        )
        success = (
            rtutils.isStructTheSame(playerTracer.memberData, testDataRaw3) and success
        )
        playerTracer.getBestMatch()
        playerTracer.exportToSM(smExportPath)
        success = (
            rtutils.isStructTheSame(playerTracer.exportData, testDataSMExport1)
            and success
        )
        exportedFileData = CsvWrpr.CsvWrpr(
            smExportPath, delHead='Index', strucType='List'
        )
        success = (
            rtutils.isStructTheSame(exportedFileData.csvDb, testDataSMExport2)
            and success
        )

        cleanup()
        playerTracer = PlayerTracer(
            chessSAMembersPath, searchedData4, searchedData4Header
        )
        success = (
            rtutils.isStructTheSame(playerTracer.memberData, testDataRaw3) and success
        )
        playerTracer.getBestMatch()
        playerTracer.exportToSM(smExportPath, p_AddRating=True)
        success = (
            rtutils.isStructTheSame(playerTracer.exportData, testDataSMExport3)
            and success
        )
        exportedFileData = CsvWrpr.CsvWrpr(
            smExportPath, delHead='Index', strucType='List'
        )
        success = (
            rtutils.isStructTheSame(exportedFileData.csvDb, testDataSMExport4)
            and success
        )

        playerTracer = PlayerTracer(chessSAMembersPath)
        CID = playerTracer.findMemberId(testfindMemberId1)
        if CID != '168008202':
            success = False
        CID = playerTracer.findMemberId(testfindMemberId2)
        if CID != '168008202':
            success = False

        cleanup()
        playerTracer = PlayerTracer(
            ursMembersPath,
            searchedData5,
            searchedData5Header,
            p_MemberDataHeader=sourceHeader2,
            p_MemberDataKey1='MemberId',
            p_MemberDataDelHead='CID',
        )
        success = (
            rtutils.isStructTheSame(playerTracer.memberData, testDataRaw4) and success
        )
        playerTracer.getBestMatch()
        playerTracer.exportToCsv(generalExportPath)
        success = (
            rtutils.isStructTheSame(playerTracer.exportData, testDataBestMatchExport5)
            and success
        )
        exportedFileData = CsvWrpr.CsvWrpr(
            generalExportPath, delHead='Do not', strucType='List'
        )
        success = (
            rtutils.isStructTheSame(exportedFileData.csvDb, testDataGeneralExport1)
            and success
        )

        playerTracer = PlayerTracer(chessSAMembersPath)
        memberDetail = {
            'Surname': 'Du Toit',
            'Name': 'Hendrik',
            'DOB': '1968/10/20',
            'MemberId': '168008202',
        }
        if not playerTracer.validateMemberId(memberDetail):
            success = False
            print('Validate id failed')
        memberDetail = {
            'Surname': 'Du Toit',
            'Name': 'Hendrik',
            'DOB': '1968/10/2',
            'MemberId': '168008',
        }
        if playerTracer.validateMemberId(memberDetail):
            success = False
            print('Validate id failed')
        memberDetail = {
            'Surname': 'Du Toi',
            'Name': 'Hendrik',
            'DOB': '1968/10/20',
            'MemberId': '168008202',
        }
        if playerTracer.validateMemberId(memberDetail):
            success = False
            print('Validate id failed')
        memberDetail = {
            'Surname': 'Du Toit',
            'Name': 'Hendri',
            'DOB': '1968/10/20',
            'MemberId': '168008202',
        }
        if playerTracer.validateMemberId(memberDetail):
            success = False
            print('Validate id failed')
        memberDetail = {
            'Surname': 'Du Toit',
            'Name': 'Hendrik',
            'DOB': '1968/10/2',
            'MemberId': '168008202',
        }
        if playerTracer.validateMemberId(memberDetail):
            success = False
            print('Validate id failed')

        if playerTracer.lookUp({'MemberId': '168008202'}, 'Region') != 'GTP':
            success = False
            print('Region LookUp failed')
        result = playerTracer.lookUp({'Region': 'GTP'}, 'MemberId')
        success = rtutils.isStructTheSame(result, lookUpResult) and success
        return success

    # end basicTest

    print('Start testing {}'.format('PlayerTracer'))
    success = basicTest()
    rtutils.resultReport(success)
    return success


# end testModule


if __name__ == '__main__':
    if sys.platform.startswith('win32'):
        baseFolder = os.path.join(
            'D:\\', 'Dropbox', 'Projects', 'PlayerTracer', '0200', 'Code'
        )
    elif sys.platform.startswith('linux'):
        baseFolder = os.path.join(
            '/home', 'hdutoit', 'Projects', 'PlayerTracer', '0200', 'Code'
        )
    palyerTracerbeetools = beetools.beetools(
        g_ClassName, g_Version, g_ClassDesc, baseFolder=baseFolder
    )
    palyerTracerbeetools = beetools.beetools(
        g_ClassName, g_Version, g_ClassDesc, baseFolder=baseFolder
    )
    palyerTracerbeetools.printHeader()
    testModule()
    palyerTracerbeetools.printFooter()
# end __main__
