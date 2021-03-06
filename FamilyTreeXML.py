#!/usr/bin/env python

#   FamilyTree
#   Copyright (C) 2015 Elstree Caldwell
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import sys
import xml.etree.ElementTree as ET
from copy import deepcopy


# ========================================================================
# Class to access family tree XML
# ========================================================================

class FamilyTreeXML( object ):


    # --------------------------------------------------------------------
    #  __init__
    # --------------------------------------------------------------------

    def __init__( self,
                  xmlFamilyTree ):

        self.ftXML = xmlFamilyTree


    # ----------------------------------------------------------------------
    def GetIndividual( self, idIndi ):

        individuals = self.GetIndividuals()

        if ( individuals is None ):
            return None

        elif ( idIndi is None ):
            return self.ftXML.find( 'INDIVIDUAL' )

        else:
            for individual in individuals:

                if ( individual.attrib['id'] == idIndi ):
                    return individual

        return None


    # ----------------------------------------------------------------------
    def GetIndividualID( self, individual ):

        return individual.attrib['id']


    # ----------------------------------------------------------------------
    def GetIndividuals( self ):

        return self.ftXML.findall( 'INDIVIDUAL' )


    # ----------------------------------------------------------------------
    def GetFamilies( self ):

        return self.ftXML.findall( 'FAMILY' )


    # ----------------------------------------------------------------------
    def GetForename(  self, individual ):

        return individual.findtext('NAME/forename')


    # ----------------------------------------------------------------------
    def GetSurname(  self, individual ):

        return individual.findtext('NAME/surname')


    # ----------------------------------------------------------------------
    def GetAlias(  self, individual ):

        return individual.findtext('ALIAS')


    # ----------------------------------------------------------------------
    def GetName(  self, individual ):

        forename = self.GetForename( individual ) or ''
        surname  = self.GetSurname( individual ) or ''

        alias = self.GetAlias( individual )

        if ( ( alias is None ) or ( len( alias ) == 0 ) ):
            return ' '.join( [ forename, surname ] )
        else:
            return ' '.join( [ forename, "'" + alias + "'", surname ] )


    # ----------------------------------------------------------------------
    def GetNameAndID(  self, individual ):

        idIndi = individual.attrib['id']

        name = self.GetName( individual )

        return ''.join( [ idIndi + '\n', name ] )

    # ----------------------------------------------------------------------
    def GetLabel(self, individual):

        label = individual.attrib['id']

        forename = self.GetForename( individual )
        surname  = self.GetSurname( individual )

        if ( ( not forename is None ) and ( len( forename ) != 0 ) ):
            label = forename + ' ' + label

        if ( ( not surname is None ) and ( len( surname ) != 0 ) ):

            if ( ( not forename is None ) and ( len( forename ) != 0 ) ):
                label = surname + ', ' + label
            else:
                label = surname + ' ' + label

        return label


    # ----------------------------------------------------------------------
    def GetNameAsSingleString(self, individual):

        label = ''

        idIndividual = individual.attrib['id']

        forename = self.GetForename( individual ).title()
        surname  = self.GetSurname( individual ).title()
        alias  = self.GetAlias( individual )

        if ( ( not surname is None ) and ( len( surname ) != 0 ) ):

            label = surname

        if ( ( not forename is None ) and ( len( forename ) != 0 ) ):

            label = label + forename

        if ( ( not alias is None ) and ( len( alias ) != 0 ) ):

            label = label + alias

        if ( len( label ) == 0 ):

            label = idIndividual

        return label.replace( ' ', '' )


    # ----------------------------------------------------------------------
    def GetFamily( self, individual, idFamilySpouse=None ):

        if ( not individual is None ):
            
            if ( idFamilySpouse is None ):
                idFamily = individual.findtext('FAMILY_SPOUSE')
                        
                if ( not idFamily is None ):

                    for family in self.GetFamilyWithID( idFamily ):
                        return family

            else:
                families = individual.findall('FAMILY_SPOUSE')
                for family in families:
                    if ( family.text == idFamilySpouse ):
                        return family

        return None

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetFamilyWithID( self, idFamily ):

        foundFamilies = []

        for family in self.GetFamilies():

            if ( family.attrib['id'] == idFamily ):
                foundFamilies.append( family )

        return foundFamilies

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetIndividualWithID( self, id ):

        foundIndividuals = []

        for individual in self.GetIndividuals():
            if ( individual.attrib['id'] == id ):
                foundIndividuals.append( individual )

        if ( len( foundIndividuals ) > 1 ):
            raise Exception( 'ERROR: Found multiple individuals with the same ID: {:s}'.format ( id ) )

        elif ( len( foundIndividuals ) == 1 ):
            return foundIndividuals[0]

        else:
            return None
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetChildWithID( self, idFamily, idIndividual ):

        children = []

        for family in self.GetFamilyWithID( idFamily ):

            for child in family.findall( 'CHILD' ):

                if ( idIndividual == child.text ):

                    return child

        return None
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def ConvertDateTupleToLabel( self, date ):

        label = None

        if ( date is None ):
            return None

        day, month, year = date

        if ( not day is None ):
            label = '{:2s}'.format( day )

        if ( not month is None ):
            if ( not label is None ):
                label = label + ' {:3s}'.format( month )
            else:
                label = month

        if ( not year is None ):
            if ( not label is None ):
                label = label + ' {:4s}'.format( year )
            else:
                label = year

        if ( not label is None ):
            return label.strip()
        else:
            return label
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetDate( self, element ):

        dateText = None

        day = None
        month = None
        year = None

        if ( element is not None ):
            date = element.find( 'DATE' )

            if ( date is not None ):

                day   = date.findtext('day')
                month = date.findtext('month')
                year  = date.findtext('year')

        return ( day, month, year )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetDateMarried( self, individual, idFamilySpouse=None ):

        spouse = None
        dateMarriage = None

        if ( idFamilySpouse is None ):
            idFamilySpouse = individual.findtext('FAMILY_SPOUSE')

        if ( idFamilySpouse ):
            for family in self.GetFamilyWithID( idFamilySpouse ):

                marriage = family.find('MARRIAGE')

                if ( not marriage is None ):
                    return self.GetDate( marriage )

        return ( None, None, None )

    # ----------------------------------------------------------------------
    def GetDateDivorced( self, individual, idFamilySpouse=None ):

        spouse = None
        dateDivorce = None

        if ( idFamilySpouse is None ):
            idFamilySpouse = individual.findtext('FAMILY_SPOUSE')

        if ( idFamilySpouse ):
            for family in self.GetFamilyWithID( idFamilySpouse ):

                divorce = family.find('DIVORCE')

                if ( not divorce is None ):
                    return self.GetDate( divorce )

        return ( None, None, None )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetOppositeSex( self, sex ):

        if ( sex == 'F' ):
            return 'M'

        elif ( sex == 'M' ):
            return 'F'

        else:
            return None

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetWife( self, individual, idFamily ):

        sex = individual.findtext('SEX')

        if ( sex == 'F' ):
            return None, None, None, None

        wife, idFamilySpouse, dateMarriage, dateDivorce = self.GetSpouse( individual, idFamily )

        return ( wife, idFamilySpouse, dateMarriage, dateDivorce )
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetWives( self, individual ):

        sex = individual.findtext('SEX')

        if ( sex == 'F' ):
            return []

        else:
            return self.GetSpouses( individual )
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetSpouse( self, individual, idFamily ):

        spouse = None
        dateMarriage = None
        dateDivorce = None

        sex = individual.findtext('SEX')

        if ( idFamily is None ): 
            idFamilySpouse = individual.findtext('FAMILY_SPOUSE')
        else:
            idFamilySpouse = idFamily
        

        if ( idFamilySpouse ):
            for family in self.GetFamilyWithID( idFamilySpouse ):

                if ( sex == 'M' ):
                    idSpouse = family.findtext('WIFE')
                else:
                    idSpouse = family.findtext('HUSBAND')

                if ( idSpouse is None ):
                    return ( None, idFamilySpouse, dateMarriage, dateDivorce )

                flgFoundSpouse = False
                for spouse in self.GetIndividuals():
                    if ( spouse.attrib['id'] == idSpouse ):
                        flgFoundSpouse = True
                        break

                if ( flgFoundSpouse ):
                    marriage = family.find('MARRIAGE')

                    if ( marriage is not None ):
                        dateMarriage = self.GetDate( marriage )

                    divorce = family.find('DIVORCE')

                    if ( divorce is not None ):
                        dateDivorce = self.GetDate( divorce )

                    break

        return ( spouse, idFamilySpouse, dateMarriage, dateDivorce )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetSpouses( self, individual ):

        spouses = []

        families = individual.findall('FAMILY_SPOUSE')
        
        for family in families:

            spouses.append( self.GetSpouse( individual, family.text ) )

        return spouses

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetChildren( self, individual, idFamily=None ):

        children = []

        if ( idFamily is None ):

            familieIDs = individual.findall('FAMILY_SPOUSE')

            families = []

            for idFamily in familieIDs:
                families = families + self.GetFamilyWithID( idFamily.text )

        else:
            families = self.GetFamilyWithID( idFamily )

        for family in families:

            for child in family.findall( 'CHILD' ):

                individualChild = self.GetIndividualWithID( child.text )
                
                if ( individualChild is not None ):
                    children.append( individualChild )

        return children

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetParents( self, individual ):

        mother = None
        father = None

        idFamilyChild  = individual.findtext('FAMILY_CHILD')

        if ( idFamilyChild ):
            for family in self.GetFamilyWithID( idFamilyChild ):

                idMother = family.findtext('WIFE')
                idFather = family.findtext('HUSBAND')

                for parent in self.GetIndividuals():
                    if ( parent.attrib['id'] == idMother ):
                        mother = parent
                    elif ( parent.attrib['id'] == idFather ):
                        father = parent

                    if ( ( mother is not None ) and ( father  is not None ) ):
                        break

        return ( mother, father, idFamilyChild )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetSiblings( self, individual ):

        siblings = []

        idFamilyChild  = individual.findtext('FAMILY_CHILD')

        if ( idFamilyChild ):

            for family in self.GetFamilyWithID( idFamilyChild ):

                for sibling in family.findall( 'CHILD' ):

                    if ( individual.attrib['id'] != sibling.text ):

                        individualSibling = self.GetIndividualWithID( sibling.text )

                        if ( individualSibling is not None ):
                            siblings.append( individualSibling )

        return ( siblings, idFamilyChild )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def CollateSubjectsSiblings( self, ftInputXML, idInputIndividual=None ):

        if ( idInputIndividual is None ):
            idInputIndividual = self.idIndividual
            
        eIndividual = self.GetIndividual( idInputIndividual )        

        idFamilyChild  = eIndividual.findtext('FAMILY_CHILD')

        if ( idFamilyChild ):

            for family in self.GetFamilyWithID( idFamilyChild ):

                for idSibling in family.findall( 'CHILD' ):

                    if ( idInputIndividual != idSibling.text ):

                        eSibling = self.GetIndividualWithID( idSibling.text )

                        if ( eSibling is not None ):
                             self.AppendIndividual( eSibling, ftInputXML )
                            
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def CollateSubjectsFamilyMembers( self, ftInputXML, idInputIndividual=None ):

        if ( idInputIndividual is None ):
            idInputIndividual = self.idIndividual
            
        eIndividual = self.GetIndividual( idInputIndividual )        

        if ( eIndividual is None ):
            return

        self.AppendIndividual( eIndividual, ftInputXML )

        sex = eIndividual.findtext('SEX')

        # Siblings

        self.CollateSubjectsSiblings( ftInputXML, idInputIndividual )
            
        # Parents

        eMother, eFather, idFamilyChild = self.GetParents( eIndividual )

        if ( not eMother is None ):

            self.AppendIndividual( eMother, ftInputXML )

        if ( not eFather is None ):

            self.AppendIndividual( eFather, ftInputXML )

        for eFamilyChild in self.GetFamilyWithID( idFamilyChild ):

            self.AppendFamily( eFamilyChild, ftInputXML )

        # Families

        idFamilies = eIndividual.findall('FAMILY_SPOUSE')

        for idFamily in idFamilies:

            for eFamily in self.GetFamilyWithID( idFamily.text ):

                self.AppendFamily( eFamily, ftInputXML )

                # Spouse
                
                if ( sex == 'M' ):
                    idSpouse = eFamily.findtext('WIFE')
                else:
                    idSpouse = eFamily.findtext('HUSBAND')

                if ( not idSpouse is None ):
                    eSpouse = self.GetIndividual( idSpouse ) 

                    self.AppendIndividual( eSpouse, ftInputXML )

                # Children

                for idChild in eFamily.findall( 'CHILD' ):

                    eChild = self.GetIndividual( idChild.text ) 

                    if ( not eChild is None ):

                        self.AppendIndividual( eChild, ftInputXML )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def GetSubjectsAncestors( self, idInputIndividual, indent=None, idAncestors=None ):

        if ( idAncestors is None ):
            idAncestors = []

        if ( indent is None ):
            indent = ''
        else:
            indent = indent + '  '

        eIndividual = self.GetIndividual( idInputIndividual )        

        if ( eIndividual is None ):
            return idAncestors

        print indent, idInputIndividual, self.GetName( eIndividual )

        eMother, eFather, idFamilyChild = self.GetParents( eIndividual )

        flgHasParent = False

        if ( not eMother is None ):
            flgHasParent = True
            idAncestors = self.GetSubjectsAncestors( eMother.attrib['id'], indent, idAncestors )
            
        if ( not eFather is None ):
            flgHasParent = True
            idAncestors = self.GetSubjectsAncestors( eFather.attrib['id'], indent, idAncestors )

        if ( not flgHasParent ):
            idAncestors.append( idInputIndividual )

        return idAncestors
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def CollateSubjectsAncestors( self, ftInputXML, idInputIndividual=None, flgIncludeSiblings=False ):

        if ( idInputIndividual is None ):
            idInputIndividual = self.idIndividual

        eIndividual = self.GetIndividual( idInputIndividual )        

        if ( eIndividual is None ):
            return
        
        self.AppendIndividual( eIndividual, ftInputXML )

        sex = eIndividual.findtext('SEX')

        # Siblings?

        if ( flgIncludeSiblings ):
            self.CollateSubjectsSiblings( ftInputXML, idInputIndividual )

        # Parents

        eMother, eFather, idFamilyChild = self.GetParents( eIndividual )

        for eFamilyChild in self.GetFamilyWithID( idFamilyChild ):

            self.AppendFamily( eFamilyChild, ftInputXML )

        if ( not eMother is None ):

            self.CollateSubjectsAncestors( ftInputXML, eMother.attrib['id'], flgIncludeSiblings )

        if ( not eFather is None ):

            self.CollateSubjectsAncestors( ftInputXML, eFather.attrib['id'], flgIncludeSiblings )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def CollateSubjectsDescendents( self, ftInputXML, idInputIndividual=None, flgIncludeSiblings=False ):

        if ( idInputIndividual is None ):
            idInputIndividual = self.idIndividual

        eIndividual = self.GetIndividual( idInputIndividual )        

        if ( eIndividual is None ):
            return

        self.AppendIndividual( eIndividual, ftInputXML )

        sex = eIndividual.findtext('SEX')

        # Siblings?

        if ( flgIncludeSiblings ):
            self.CollateSubjectsSiblings( ftInputXML, idInputIndividual )


        # Families

        idFamilies = eIndividual.findall('FAMILY_SPOUSE')

        for idFamily in idFamilies:

            for eFamily in self.GetFamilyWithID( idFamily.text ):

                self.AppendFamily( eFamily, ftInputXML )

                # Spouse
                
                if ( sex == 'M' ):
                    idSpouse = eFamily.findtext('WIFE')
                else:
                    idSpouse = eFamily.findtext('HUSBAND')

                if ( not idSpouse is None ):
                    eSpouse = self.GetIndividual( idSpouse ) 

                    self.AppendIndividual( eSpouse, ftInputXML )

                # Children

                for idChild in eFamily.findall( 'CHILD' ):

                    eChild = self.GetIndividual( idChild.text ) 

                    if ( not eChild is None ):

                        self.CollateSubjectsDescendents( ftInputXML, idChild.text, flgIncludeSiblings )

    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def CreateIndividual( self, idFamilyChild=None, idFamilySpouse=None ):

        ids = []
        for individual in self.GetIndividuals():
            ids.append( individual.attrib['id'] )

        i = 1
        idIndi = 'I{:03d}'.format ( i )
        while ( idIndi in ids ):
            i = i + 1
            idIndi = 'I{:03d}'.format ( i )

        return ET.SubElement( self.ftXML, 'INDIVIDUAL', { 'id': idIndi } )
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def CreateFamily( self, individual=None ):

        ids = []
        for family in self.GetFamilies():
            ids.append( family.attrib['id'] )

        i = 1
        idFamily = 'F{:03d}'.format ( i )
        while ( idFamily in ids ):
            i = i + 1
            idFamily = 'F{:03d}'.format ( i )

        eFamily = ET.SubElement( self.ftXML, 'FAMILY', { 'id': idFamily } )

        # Assign the id to this individual

        if ( not individual is None ):

            eFamilySpouse = ET.SubElement( individual, 'FAMILY_SPOUSE' )

            eFamilySpouse.text = idFamily


        return eFamily
   # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def DeleteFamily( self, idFamily ):

        if ( not idFamily is None ):

            for family in self.GetFamilyWithID( idFamily ):

                print 'DeleteFamily: Deleting family', idFamily
                ET.dump( family )
                self.ftXML.remove( family )

            for individual in self.GetIndividuals():

                print '\nDeleteFamily: Individual'
                ET.dump( individual )

                families = individual.findall('FAMILY_SPOUSE')

                for family in families:

                    if ( family.text == idFamily ):
                        print 'DeleteFamily: Deleting spouse', family.text
                        ET.dump( family )
                        individual.remove( family )

                families = individual.findall('FAMILY_CHILD')

                for family in families:

                    if ( family.text == idFamily ):
                        print 'DeleteFamily: Deleting child', family.text
                        ET.dump( family )
                        individual.remove( family )


    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    def DeleteIndividual( self, idIndividual ):

        prevIndividual = None
        theIndividual  = None
        nextIndividual = None

        lastIndividual = None

        # Find the individual

        for individual in self.GetIndividuals():

            if ( individual.attrib['id'] == idIndividual ):

                theIndividual = individual
                prevIndividual = lastIndividual

            elif ( not theIndividual is None ):

                nextIndividual = individual
                break

            lastIndividual = individual

        self.ftXML.remove( theIndividual )

        # Also delete spouse references

        idFamilySpouse = theIndividual.findtext('FAMILY_SPOUSE')

        for family in self.GetFamilyWithID( idFamilySpouse ):

            if ( idIndividual == family.findtext('WIFE') ):

                eWife = family.find('WIFE')
                family.remove( eWife )

            if ( idIndividual == family.findtext('HUSBAND') ):

                eHusband = family.find('HUSBAND')
                family.remove( eHusband )

            # If the family has no spouses or children then delete is

            if ( ( family.findtext('WIFE') is None ) and
                 ( family.findtext('HUSBAND') is None ) and
                 ( family.findtext('CHILD') is None ) ):

                self.ftXML.remove( family )

        # and child references

        idFamilyChild = theIndividual.findtext('FAMILY_CHILD')

        for family in self.GetFamilyWithID( idFamilyChild ):

            if ( idIndividual == family.findtext('CHILD') ):

                eChild = family.find('CHILD')
                family.remove( eChild )

            # If the family has no spouses or children then delete is

            if ( ( family.findtext('WIFE') is None ) and
                 ( family.findtext('HUSBAND') is None ) and
                 ( family.findtext('CHILD') is None ) ):

                self.ftXML.remove( family )


        # Return the id of an adjacent individual

        if ( not prevIndividual is None ):
            return prevIndividual.attrib['id']

        elif ( not nextIndividual is None ):
            return nextIndividual.attrib['id']

        return None


    # ----------------------------------------------------------------------
    def SetFirstName( self, idIndividual, name ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eName = theIndividual.find('NAME')

            if ( eName is None ):
                eName = ET.SubElement( theIndividual, 'NAME' )

            eFirstName = eName.find('forename')

            if ( eFirstName is None ):
                eFirstName = ET.SubElement( eName, 'forename' )

            eFirstName.text = name


    # ----------------------------------------------------------------------
    def SetLastName( self, idIndividual, name ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eName = theIndividual.find('NAME')

            if ( eName is None ):
                eName = ET.SubElement( theIndividual, 'NAME' )

            eLastName = eName.find('surname')

            if ( eLastName is None ):
                eLastName = ET.SubElement( eName, 'surname' )

            eLastName.text = name


    # ----------------------------------------------------------------------
    def SetAlias( self, idIndividual, alias ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eAlias = theIndividual.find('ALIAS')

            if ( eAlias is None ):
                eAlias = ET.SubElement( theIndividual, 'ALIAS' )

            eAlias.text = alias


    # ----------------------------------------------------------------------
    def SetSex( self, idIndividual, sex ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eSex = theIndividual.find('SEX')

            if ( eSex is None ):
                eSex = ET.SubElement( theIndividual, 'SEX' )

            eSex.text = sex


    # ----------------------------------------------------------------------
    def SetDay( self, element, day ):

        eDate = element.find('DATE')

        if ( eDate is None ):
            eDate = ET.SubElement(element, 'DATE' )

        eDay  = eDate.find('day')

        if ( eDay is None ):
            eDay = ET.SubElement(eDate, 'day' )

        eDay.text = day


    # ----------------------------------------------------------------------
    def SetMonth( self, element, month ):

        eDate = element.find('DATE')

        if ( eDate is None ):
            eDate = ET.SubElement(element, 'DATE' )

        eMonth  = eDate.find('month')

        if ( eMonth is None ):
            eMonth = ET.SubElement(eDate, 'month' )

        eMonth.text = month


    # ----------------------------------------------------------------------
    def SetYear( self, element, year ):

        eDate = element.find('DATE')

        if ( eDate is None ):
            eDate = ET.SubElement(element, 'DATE' )

        eYear  = eDate.find('year')

        if ( eYear is None ):
            eYear = ET.SubElement(eDate, 'year' )

        eYear.text = year



    # ----------------------------------------------------------------------
    def SetDate( self, element, day, month, year ):

        self.SetDay(   element, day )
        self.SetMonth( element, month )
        self.SetYear(  element, year )


    # ----------------------------------------------------------------------
    def SetBirthDay( self, idIndividual, day ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eBirth = theIndividual.find('BIRTH')

            if ( eBirth is None ):
                eBirth = ET.SubElement( theIndividual, 'BIRTH' )

            self.SetDay( eBirth, day )


    # ----------------------------------------------------------------------
    def SetBirthMonth( self, idIndividual, month ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eBirth = theIndividual.find('BIRTH')

            if ( eBirth is None ):
                eBirth = ET.SubElement(theIndividual, 'BIRTH' )

            self.SetMonth( eBirth, month )


    # ----------------------------------------------------------------------
    def SetBirthYear( self, idIndividual, year ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eBirth = theIndividual.find('BIRTH')

            if ( eBirth is None ):
                eBirth = ET.SubElement(theIndividual, 'BIRTH' )

            self.SetYear( eBirth, year )


    # ----------------------------------------------------------------------
    def SetBirthPlace( self, idIndividual, place ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eBirth = theIndividual.find('BIRTH')

            if ( eBirth is None ):
                eBirth = ET.SubElement(theIndividual, 'BIRTH' )

            ePlace = eBirth.find('PLACE')

            if ( ePlace is None ):
                ePlace = ET.SubElement(eBirth, 'PLACE' )

            ePlace.text = place


    # ----------------------------------------------------------------------
    def SetDeathDay( self, idIndividual, day ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eDeath = theIndividual.find('DEATH')

            if ( eDeath is None ):
                eDeath = ET.SubElement(theIndividual, 'DEATH' )

            self.SetDay( eDeath, day )


    # ----------------------------------------------------------------------
    def SetDeathMonth( self, idIndividual, month ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eDeath = theIndividual.find('DEATH')

            if ( eDeath is None ):
                eDeath = ET.SubElement(theIndividual, 'DEATH' )

            self.SetMonth( eDeath, month )


    # ----------------------------------------------------------------------
    def SetDeathYear( self, idIndividual, year ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eDeath = theIndividual.find('DEATH')

            if ( eDeath is None ):
                eDeath = ET.SubElement(theIndividual, 'DEATH' )

            self.SetYear( eDeath, year )


    # ----------------------------------------------------------------------
    def SetDeathPlace( self, idIndividual, place ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eDeath = theIndividual.find('DEATH')

            if ( eDeath is None ):
                eDeath = ET.SubElement(theIndividual, 'DEATH' )

            ePlace = eDeath.find('PLACE')

            if ( ePlace is None ):
                ePlace = ET.SubElement(eDeath, 'PLACE' )

            ePlace.text = place


    # ----------------------------------------------------------------------
    def SetBurialPlace( self, idIndividual, place ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eBurial = theIndividual.find('BURIAL')

            if ( eBurial is None ):
                eBurial = ET.SubElement(theIndividual, 'BURIAL' )

            ePlace = eBurial.find('PLACE')

            if ( ePlace is None ):
                ePlace = ET.SubElement(eBurial, 'PLACE' )

            ePlace.text = place


    # ----------------------------------------------------------------------
    def SetDivorcedDay( self, idIndividual, day, idFamily ):

        self.SetMarriedDay( idIndividual, day, idFamily, True )


    # ----------------------------------------------------------------------
    def SetSubjectNote( self, idIndividual, note ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            eNote = theIndividual.find('NOTE')

            if ( eNote is None ):
                eNote = ET.SubElement( theIndividual, 'NOTE' )

            eNote.text = note


    # ----------------------------------------------------------------------
    def SetFamilyNote( self, idIndividual, idFamily, note ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            theFamily = self.GetFamily( theIndividual, idFamily )

            if ( not theFamily is None ):
                eNote = theFamily.find('NOTE')

                if ( eNote is None ):
                    eNote = ET.SubElement( theFamily, 'NOTE' )

                eNote.text = note


    # ----------------------------------------------------------------------
    def SetMarriedDay( self, idIndividual, day, idFamily, flgDivorced=False ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            sex = theIndividual.findtext('SEX')

            if ( idFamily is None ):
                idFamily = theIndividual.findtext('FAMILY_SPOUSE')

            if ( idFamily is None ):

                family = self.CreateFamily( theIndividual )
                idFamily = family.attrib['id']


            for family in self.GetFamilyWithID( idFamily ):

                eSpouse = None

                if ( sex == 'F' ):

                    eSpouse = family.find('WIFE')

                    if ( eSpouse is None ):
                        eSpouse = ET.SubElement( family, 'WIFE' )

                elif ( sex == 'M' ):
                    eSpouse = family.find('HUSBAND')

                    if ( eSpouse is None ):
                        eSpouse = ET.SubElement( family, 'HUSBAND' )

                if ( not eSpouse is None ):
                    eSpouse.text = idIndividual

                if ( flgDivorced ):
                    eMarried = family.find('DIVORCE')
                else:
                    eMarried = family.find('MARRIAGE')

                if ( eMarried is None ):
                    if ( flgDivorced ):
                        eMarried = ET.SubElement( family, 'DIVORCE' )
                    else:
                        eMarried = ET.SubElement( family, 'MARRIAGE' )

                self.SetDay( eMarried, day )


    # ----------------------------------------------------------------------
    def SetDivorcedMonth( self, idIndividual, month, idFamily ):

        self.SetMarriedMonth( idIndividual, month, idFamily, True )


    # ----------------------------------------------------------------------
    def SetMarriedMonth( self, idIndividual, month, idFamily, flgDivorced=False ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            sex = theIndividual.findtext('SEX')

            if ( idFamily is None ):
                idFamily = theIndividual.findtext('FAMILY_SPOUSE')

            if ( idFamily is None ):

                family = self.CreateFamily( theIndividual )
                idFamily = family.attrib['id']

            for family in self.GetFamilyWithID( idFamily ):

                eSpouse = None

                if ( sex == 'F' ):

                    eSpouse = family.find('WIFE')

                    if ( eSpouse is None ):
                        eSpouse = ET.SubElement( family, 'WIFE' )

                elif ( sex == 'M' ):
                    eSpouse = family.find('HUSBAND')

                    if ( eSpouse is None ):
                        eSpouse = ET.SubElement( family, 'HUSBAND' )

                if ( not eSpouse is None ):
                    eSpouse.text = idIndividual


                if ( flgDivorced ):
                    eMarried = family.find('DIVORCE')
                else:
                    eMarried = family.find('MARRIAGE')

                if ( eMarried is None ):
                    if ( flgDivorced ):
                        eMarried = ET.SubElement( family, 'DIVORCE' )
                    else:
                        eMarried = ET.SubElement( family, 'MARRIAGE' )

                self.SetMonth( eMarried, month )


    # ----------------------------------------------------------------------
    def SetDivorcedYear( self, idIndividual, year, idFamily ):

        self.SetMarriedYear( idIndividual, year, idFamily, True )


    # ----------------------------------------------------------------------
    def SetMarriedYear( self, idIndividual, year, idFamily, flgDivorced=False ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            sex = theIndividual.findtext('SEX')

            if ( idFamily is None ):
                idFamily = theIndividual.findtext('FAMILY_SPOUSE')

            if ( idFamily is None ):

                family = self.CreateFamily( theIndividual )
                idFamily = family.attrib['id']

            for family in self.GetFamilyWithID( idFamily ):

                eSpouse = None

                if ( sex == 'F' ):

                    eSpouse = family.find('WIFE')

                    if ( eSpouse is None ):
                        eSpouse = ET.SubElement( family, 'WIFE' )

                elif ( sex == 'M' ):
                    eSpouse = family.find('HUSBAND')

                    if ( eSpouse is None ):
                        eSpouse = ET.SubElement( family, 'HUSBAND' )

                if ( not eSpouse is None ):
                    eSpouse.text = idIndividual

                if ( flgDivorced ):
                    eMarried = family.find('DIVORCE')
                else:
                    eMarried = family.find('MARRIAGE')

                if ( eMarried is None ):
                    if ( flgDivorced ):
                        eMarried = ET.SubElement( family, 'DIVORCE' )
                    else:
                        eMarried = ET.SubElement( family, 'MARRIAGE' )

                self.SetYear( eMarried, year )


    # ----------------------------------------------------------------------
    def SetMarriedPlace( self, idIndividual, idFamily, place ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            theFamily = self.GetFamily( theIndividual, idFamily )

            if ( theFamily is None ):

                theFamily = self.CreateFamily( theIndividual )

            eMarriage = theFamily.find('MARRIAGE')

            if ( eMarriage is None ):
                eMarriage = ET.SubElement(theIndividual, 'MARRIAGE' )

            ePlace = eMarriage.find('PLACE')

            if ( ePlace is None ):
                ePlace = ET.SubElement(eMarriage, 'PLACE' )

            ePlace.text = place


    # ----------------------------------------------------------------------
    def SetFather( self, idIndividual, idFather ):

        theIndividual = self.GetIndividual( idIndividual )
        theFather     = self.GetIndividual( idFather )

        families = []

        if ( not theIndividual is None ):

            # Get the individual's family

            idFamily  = theIndividual.findtext('FAMILY_CHILD')

            # Try the father's family

            if ( idFamily is None ):

                idFamily  = theFather.findtext('FAMILY_SPOUSE')
                fathersFamily = self.GetFamilyWithID( idFamily )

                for family in fathersFamily:

                    eChild = self.GetChildWithID( idFamily, idIndividual )

                    if ( eChild is None ):
                        eChild = ET.SubElement( family, 'CHILD' )
                        eChild.text = idIndividual

                    eFamilyChild = ET.SubElement( theIndividual, 'FAMILY_CHILD' )
                    eFamilyChild.text = idFamily

                    families.append( family )

            # Neither individual or father have appropriate families so create a new one

            if ( idFamily is None ):

                family = self.CreateFamily()
                idFamily = family.attrib['id']

                eChild = ET.SubElement( family, 'CHILD' )
                eChild.text = idIndividual

                eFamilyChild = ET.SubElement( theIndividual, 'FAMILY_CHILD' )
                eFamilyChild.text = idFamily

                families.append( family )

            else:

                families = self.GetFamilyWithID( idFamily )


            for family in families:

                eHusband = family.find( 'HUSBAND' )

                if ( eHusband is None ):
                    eHusband = ET.SubElement( family, 'HUSBAND' )

                eHusband.text = idFather


            eFamilySpouse = theFather.find( 'FAMILY_SPOUSE' )

            if ( eFamilySpouse is None ):
                eFamilySpouse = ET.SubElement( theFather, 'FAMILY_SPOUSE' )

            eFamilySpouse.text = idFamily

        else:
            print 'SetFather(', idIndividual, idFather, ') Individual is none:'


    # ----------------------------------------------------------------------
    def SetMother( self, idIndividual, idMother ):

        theIndividual = self.GetIndividual( idIndividual )
        theMother     = self.GetIndividual( idMother )

        families = []

        if ( not theIndividual is None ):

            # Get the individual's family

            idFamily  = theIndividual.findtext('FAMILY_CHILD')

            # Try the mother's family

            if ( idFamily is None ):

                idFamily  = theMother.findtext('FAMILY_SPOUSE')
                mothersFamily = self.GetFamilyWithID( idFamily )

                for family in mothersFamily:

                    eChild = self.GetChildWithID( idFamily, idIndividual )

                    if ( eChild is None ):
                        eChild = ET.SubElement( family, 'CHILD' )
                        eChild.text = idIndividual

                    eFamilyChild = ET.SubElement( theIndividual, 'FAMILY_CHILD' )
                    eFamilyChild.text = idFamily

                    families.append( family )

            # Neither individual or mother have appropriate families so create a new one

            if ( idFamily is None ):

                family = self.CreateFamily()
                idFamily = family.attrib['id']

                eChild = ET.SubElement( family, 'CHILD' )
                eChild.text = idIndividual

                eFamilyChild = ET.SubElement( theIndividual, 'FAMILY_CHILD' )
                eFamilyChild.text = idFamily

                families.append( family )

            else:

                families = self.GetFamilyWithID( idFamily )


            for family in families:

                eWife = family.find( 'WIFE' )

                if ( eWife is None ):
                    eWife = ET.SubElement( family, 'WIFE' )

                eWife.text = idMother


            eFamilySpouse = theMother.find( 'FAMILY_SPOUSE' )

            if ( eFamilySpouse is None ):
                eFamilySpouse = ET.SubElement( theMother, 'FAMILY_SPOUSE' )

            eFamilySpouse.text = idFamily

        else:
            print 'SetMother(', idIndividual, idMother, ') Individual is none:'


    # ----------------------------------------------------------------------
    def SetSpouse( self, idIndividual, idSpouse, idFamilySpouse=None ):

        theIndividual = self.GetIndividual( idIndividual )
        theSpouse     = self.GetIndividual( idSpouse )

        if ( not theIndividual is None ):

            sexIndividual = theIndividual.findtext('SEX')
            sexSpouse     = theSpouse.findtext('SEX')

            if ( ( sexIndividual is None ) and ( sexSpouse is None ) ):
                print 'SetSpouse(', idIndividual, idSpouse, ') Genders not set, cannot set spouse'
                return

            if ( ( sexIndividual == 'M' ) and ( sexSpouse == 'M' ) ):
                print 'SetSpouse(', idIndividual, idSpouse, ') Genders are both male'
                return
            elif ( ( sexIndividual == 'F' ) and ( sexSpouse == 'F' ) ):
                print 'SetSpouse(', idIndividual, idSpouse, ') Genders are both female'
                return

            if ( ( sexIndividual is None ) and ( not sexSpouse is None ) ):
                sexIndividual = self.GetOppositeSex( sexSpouse )
                self.SetSex( theIndividual, sexIndividual )

            if ( ( sexSpouse is None ) and ( not sexIndividual is None ) ):
                sexSpouse = self.GetOppositeSex( sexIndividual )
                self.SetSex( theSpouse, sexSpouse )


            # Get the individual's family

            if ( idFamilySpouse is None ):
                idFamily  = theIndividual.findtext('FAMILY_SPOUSE')
            else:
                idFamily = idFamilySpouse

            if ( idFamily is None ):
                idFamily  = theSpouse.findtext('FAMILY_SPOUSE')

            if ( idFamily is None ):

                family = self.CreateFamily()
                families = [ family ]

            else:

                families = self.GetFamilyWithID( idFamily )


            for family in families:

                idFamily = family.attrib['id']

                eWife =  family.find( 'WIFE' )

                if ( eWife is None ):
                    eWife = ET.SubElement( family, 'WIFE' )

                eHusband = family.find( 'HUSBAND' )

                if ( eHusband is None ):
                    eHusband = ET.SubElement( family, 'HUSBAND' )

                if ( sexIndividual == 'F' ):
                    eWife.text = idIndividual
                    eHusband.text = idSpouse
                else:
                    eWife.text = idSpouse
                    eHusband.text = idIndividual


            eFamilySpouse = self.GetFamily( theIndividual, idFamily )

            if ( eFamilySpouse is None ):
                
                eFamilySpouse = ET.SubElement( theIndividual, 'FAMILY_SPOUSE' )
                eFamilySpouse.text = idFamily


            eFamilySpouse = self.GetFamily( theSpouse, idFamily )

            if ( eFamilySpouse is None ):
                
                eFamilySpouse = ET.SubElement( theSpouse, 'FAMILY_SPOUSE' )
                eFamilySpouse.text = idFamily


        else:
            print 'SetSpouse(', idIndividual, idSpouse, ') Individual is none:'


    # ----------------------------------------------------------------------
    def SetChild( self, idIndividual, idChild, idFamily=None ):

        theIndividual = self.GetIndividual( idIndividual )
        theChild = self.GetIndividual( idChild )

        sexIndividual = theIndividual.findtext('SEX')

        # Does the parent have a family already?

        if ( idFamily is None ):
            idFamily  = theIndividual.findtext('FAMILY_SPOUSE')

        # If not then perhaps the child

        if ( idFamily is None ):

            idFamily  = theChild.findtext('FAMILY_CHILD')

            if ( idFamily is None ):

                family = self.CreateFamily()
                idFamily = family.attrib['id']

            for family in self.GetFamilyWithID( idFamily ):

                eFamilySpouse = ET.SubElement( theIndividual, 'FAMILY_SPOUSE' )
                eFamilySpouse.text = idFamily

                if ( sexIndividual == 'F' ):
                    eWife =  family.find( 'WIFE' )

                    if ( eWife is None ):
                        eWife = ET.SubElement( family, 'WIFE' )

                    eWife.text = idIndividual
                else:
                    eHusband = family.find( 'HUSBAND' )

                    if ( eHusband is None ):
                        eHusband = ET.SubElement( family, 'HUSBAND' )

                    eHusband.text = idIndividual

        # Parent has a family so add the child

        flgChildFound = False

        for family in self.GetFamilyWithID( idFamily ):

            for child in family.findall( 'CHILD' ):

                if ( child.text == idChild ):
                    flgChildFound = True

            if ( not flgChildFound ):

                eFamilyChild = ET.SubElement( family, 'CHILD' )
                eFamilyChild.text = idChild

            if ( sexIndividual == 'F' ):
                eWife =  family.find( 'WIFE' )

                if ( eWife is None ):
                    eWife = ET.SubElement( family, 'WIFE' )

                eWife.text = idIndividual
            else:
                eHusband = family.find( 'HUSBAND' )

                if ( eHusband is None ):
                    eHusband = ET.SubElement( family, 'HUSBAND' )

                eHusband.text = idIndividual

        eChild = theChild.find( 'FAMILY_CHILD' )

        if ( eChild is None ):
            eChild = ET.SubElement( theChild, 'FAMILY_CHILD' )

        eChild.text = idFamily


    # ----------------------------------------------------------------------
    def RemoveParents( self, idIndividual ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            idFamily  = theIndividual.findtext('FAMILY_CHILD')

            if ( not idFamily is None ):

                for family in self.GetFamilyWithID( idFamily ):

                    for child in family.findall( 'CHILD' ):

                        idChild = child.text

                        if ( idChild == idIndividual ):

                            family.remove( child )

                    # If the family has no spouses or children then delete is

                    if ( ( family.findtext('WIFE') is None ) and
                         ( family.findtext('HUSBAND') is None ) and
                         ( family.findtext('CHILD') is None ) ):

                        self.ftXML.remove( family )


                eFamilyChild = theIndividual.find('FAMILY_CHILD')

                theIndividual.remove( eFamilyChild )


    # ----------------------------------------------------------------------
    def RemoveSpouse( self, idIndividual ):

        theIndividual = self.GetIndividual( idIndividual )

        if ( not theIndividual is None ):

            sex = theIndividual.findtext('SEX')

            idFamily  = theIndividual.findtext('FAMILY_SPOUSE')

            if ( not idFamily is None ):

                for family in self.GetFamilyWithID( idFamily ):

                    if ( sex == 'F' ):
                        eSpouse = family.find('WIFE')
                    else:
                        eSpouse = family.find('HUSBAND')

                    if ( not eSpouse is None ):
                        idSpouse = eSpouse.text

                        if ( idSpouse == idIndividual ):

                            family.remove( eSpouse )

                    # If the family has no spouses or children then delete is

                    if ( ( family.findtext('WIFE') is None ) and
                         ( family.findtext('HUSBAND') is None ) and
                         ( family.findtext('CHILD') is None ) ):

                        self.ftXML.remove( family )


                eFamilySpouse = theIndividual.find('FAMILY_SPOUSE')

                theIndividual.remove( eFamilySpouse )


    # ----------------------------------------------------------------------
    def RemoveChild( self, idParent, idChild ):

        theParent = self.GetIndividual( idParent )
        theChild = self.GetIndividual( idChild )

        if ( not theParent is None ):

            idFamily  = theParent.findtext('FAMILY_SPOUSE')

            if ( idFamily is None ):

                idFamily  = theChild.findtext('FAMILY_CHILD')

            if ( not idFamily is None ):

                for family in self.GetFamilyWithID( idFamily ):

                    for child in family.findall( 'CHILD' ):

                        idc = child.text

                        if ( idChild == idc ):

                            family.remove( child )

                eFamilyChild = theChild.find('FAMILY_CHILD')

                theChild.remove( eFamilyChild )


    # ----------------------------------------------------------------------
    def AppendIndividual( self, newIndividual, ftInputXML=None ):

        if ( ftInputXML is None ):
            ftInputXML = self.ftXML

        individuals = ftInputXML.findall( 'INDIVIDUAL' )

        if ( individuals is None ):
            ftInputXML.append( deepcopy( newIndividual ) )
            return

        idNewIndividual = newIndividual.attrib['id']

        flgFound = False
        for individual in individuals:

            if ( individual.attrib['id'] == idNewIndividual ):
                flgFound = True
                break

        if ( not flgFound ):
            ftInputXML.append( deepcopy( newIndividual ) )

    # ----------------------------------------------------------------------
    def AppendFamily( self, newFamily, ftInputXML=None ):

        if ( ftInputXML is None ):
            ftInputXML = self.ftXML

        families = ftInputXML.findall( 'FAMILY' )

        if ( families is None ):
            ftInputXML.append( deepcopy( newFamily ) )
            return

        idNewFamily = newFamily.attrib['id']

        flgFound = False
        for family in families:

            if ( family.attrib['id'] == idNewFamily ):
                flgFound = True
                break

        if ( not flgFound ):
            ftInputXML.append( deepcopy( newFamily ) )

