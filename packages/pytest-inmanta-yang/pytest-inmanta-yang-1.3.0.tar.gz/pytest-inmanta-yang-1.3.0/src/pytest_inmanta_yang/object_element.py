"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import logging
import re
from abc import abstractmethod
from typing import Generator, Generic, Iterator, List, Optional, TypeVar, Union

from lxml import etree, objectify  # type: ignore

LOGGER = logging.getLogger(__name__)

ElementType = Union["ObjectElement", str, bool, int, float, None]
PrimitiveType = Union[str, bool, int, float]


T = TypeVar("T", bound=object)


class SkipSubElement(ValueError):
    """
    This exception is raised when a child from a object element can't be wrapped
    """


class SubElement(Generic[T]):
    """
    This abstract class is an abstraction layer that allows to get access to certain
    types of object children.  The type of resource to be returned is determined by
    the subclass.
    """

    TAG_REGEX = re.compile(r"{(.*)}(.*)")
    """
    Regular expression allowing to match tags and extract the inner name and namespace.
    A tag should be formed like this: {<namespace>}<name>
    e.g.    {http://cisco.com/ns/yang/Cisco-IOS-XR-aaa-locald-admin-cfg}aaa
            where   http://cisco.com/ns/yang/Cisco-IOS-XR-aaa-locald-admin-cfg  is the namespace
            and     aaa                                                         is the name
    """

    def __init__(self, parent: objectify.ObjectifiedDataElement) -> None:
        """
        :param parent: The object whose children we are trying to get
        """
        self._parent = parent

    @abstractmethod
    def _wrap(self, item: objectify.ObjectifiedDataElement) -> T:
        """
        Wrap a child item and ensure it is of the expected type.  If the type is not right
        the method should raise SkipSubElement exception.
        """

    def __iter__(self) -> Generator[T, None, None]:
        """Returns a generator to loop over the children matching the expected type (if any)"""
        for item in self._parent.getchildren():
            try:
                yield self._wrap(item)
            except SkipSubElement:
                pass

    def get_subelements(
        self, name: str, namespace: Optional[str] = None
    ) -> Generator[T, None, None]:
        """
        Search for all subelements in the children of this element whose tag contain the provided name
        and namespace (if provided).

        :param name: The name of the child element
        :param namespace: The namespace of the child element
        """
        children: List[objectify.ObjectifiedDataElement] = self._parent.getchildren()
        for child in children:
            tag_match = self.TAG_REGEX.match(child.tag)
            if not tag_match:
                LOGGER.warning(
                    f"The following tag didn't match the expected format: {child.tag}.  "
                    "It will be skipped."
                )
                continue

            child_namespace, child_name = tag_match.groups()

            if name != child_name:
                # The name doesn't match
                continue

            if namespace is not None and namespace != child_namespace:
                # The namespace doesn't match
                continue

            try:
                yield self._wrap(child)
            except SkipSubElement:
                pass

    def get_subelement(self, name: str, namespace: Optional[str] = None) -> Optional[T]:
        """
        Search for a subelement in the children of this element. If the provided name is unique it will
        return it, even if no namespace is provided.

        If multiple children matching the name and namespace are found, and Exception is raised.
        If no child matching the name and namespace is found, None is returned.

        :param name: The name of the child element
        :param namespace: The namespace of the child element
        """
        all_sub_elements = [elem for elem in self.get_subelements(name, namespace)]
        if len(all_sub_elements) > 1:
            raise Exception(
                f"Found multiple elements for tag {{{namespace or '*'}}}{name}: "
                f"{[s for s in all_sub_elements]}"
            )

        if not all_sub_elements:
            return None

        return all_sub_elements[0]


class Attribute(SubElement[PrimitiveType]):
    """
    This subclass of SubElement ensures that the returned type will be a value with a primitive type

    This corresponds to single value children in a xml obj, by opposition to nested obj children.
    """

    def _wrap(self, item: objectify.ObjectifiedDataElement) -> PrimitiveType:
        if item.text is None:
            # If we don't have a text field, the item is a xml object
            raise SkipSubElement()

        return item.pyval


class Relation(SubElement["ObjectElement"]):
    """
    This subclass of SubElement ensures that the returned type will be a nested xml object
    """

    def _wrap(self, item: objectify.ObjectifiedDataElement) -> "ObjectElement":
        if item.text is not None:
            # If we have a text field, the item is an xml object attribute
            raise SkipSubElement()

        return ObjectElement(item)


class SubElementItem(SubElement[T]):
    """
    This is an abstract subclass of SubElement, for all children (identified by object tag) that are expected
    to be found only once in the xml object.
    The element can be accessed as if it was an attribute of this object, using its name as attribute name.
    If the child name contains any "-", the attribute name in python should contain a "_" in place.

        e.g.:

            xml_obj = objectify.fromstring(
                '''
                    <child>
                        <name>Bob</name>
                        <dad>
                            <name>Chris</name>
                        </dad>
                    </child>
                '''
            )
            child_element = ObjectElement(xml_obj)

            # The child name is an attribute
            assert child_element.attributes.name == "Bob"

            # The dad is an object, the dad name is one of its attribute
            assert child_element.relations.dad.attributes.name == "Chris"

    """

    def __getattr__(self, name: str) -> T:
        """
        Get a child of this element. When an underscore is provided and the lookup fails a lookup
        with - will be done.
        """
        ele = self.get_subelement(name)
        if ele is None:
            if "_" in name:
                return self.__getattr__(name.replace("_", "-"))
            else:
                raise AttributeError(
                    f"Element {repr(self._parent)} does not have a child {name}"
                )

        return ele

    def __getitem__(self, key: Union[int, str]) -> T:
        """
        Support using object[something]. When a string is provided a child element lookup is performed. When
        a number is provided a list lookup is performed.
        """
        if isinstance(key, int):
            for position, item in enumerate(iter(self)):
                if position == key:
                    return item

            raise IndexError()

        return self.__getattr__(key)


class AttributeItem(Attribute, SubElementItem[PrimitiveType]):
    """
    This SubElement implementation allows to access unique attribute in a xml object
    """


class RelationItem(Relation, SubElementItem["ObjectElement"]):
    """
    This SubElement implementation allows to access unique nested object in a xml object
    """


class SubElementList(SubElement[T]):
    """
    This is an abstract subclass of SubElement, for all children (identified by object tag) that are expected
    to be found only once in the xml object.
    The element can be accessed as if it was an attribute of this object, using its name as attribute name.
    If the child name contains any "-", the attribute name in python should contain a "_" in place.

        e.g.:

            xml_obj = objectify.fromstring(
                '''
                    <dad>
                        <name>Steven</name>
                        <surname>Dad</surname>
                        <surname>Steve</surname>
                        <child>
                            <name>Chris</name>
                        </child>
                        <child>
                            <name>Elise</name>
                        </child>
                    </dad>
                '''
            )
            dad_element = ObjectElement(xml_obj)

            # The dad surnames are a list of attributes
            assert dad_element.list_attributes.surname == ["Dad", "Steve"]

            # Single item can still be accessed as a list
            assert dad_element.list_attributes.name == ["Steven"]

            # The child is a nested object, that can be found multiple times
            assert [child.attributes.name for child in dad_element.relations.child] == ["Chris", "Elise"]

    """

    def __getattr__(self, name: str) -> List[T]:
        """Get a child of this element. When an underscore is provided and the lookup fails a lookup
        with - will be done.
        """
        elements = [e for e in self.get_subelements(name)]
        if "_" in name:
            elements += [e for e in self.get_subelements(name.replace("_", "-"))]

        return elements

    def __getitem__(self, key: Union[int, str]) -> List[T]:
        """Support using object[something]. When a string is provided a child element lookup is performed. When
        a number is provided a list lookup is performed.
        """
        if isinstance(key, int):
            for position, item in enumerate(iter(self)):
                if position == key:
                    return [item]

            raise IndexError()

        return self.__getattr__(key)


class AttributeList(Attribute, SubElementList[PrimitiveType]):
    """
    This SubElement implementation allows to access attributes in a xml object that can
    be found more than once by parent object.
    """


class RelationList(Relation, SubElementList["ObjectElement"]):
    """
    This SubElement implementation allows to access nested objects in a xml object that can
    be found more than once by parent object.
    """


class ObjectElement:
    """A wrapper object for the lxml objectify function"""

    TAG_REGEX = re.compile(r"{(.*)}(.*)")
    """
    Regular expression allowing to match tags and extract the inner name and namespace.
    A tag should be formed like this: {<namespace>}<name>
    e.g.    {http://cisco.com/ns/yang/Cisco-IOS-XR-aaa-locald-admin-cfg}aaa
            where   http://cisco.com/ns/yang/Cisco-IOS-XR-aaa-locald-admin-cfg  is the namespace
            and     aaa                                                         is the name
    """

    def __init__(self, lxml_object: objectify.ObjectifiedDataElement) -> None:
        self._object = lxml_object

        match = self.TAG_REGEX.match(lxml_object.tag)
        assert match is not None, f"Invalid tag: {lxml_object.tag}"
        self._namespace, self._name = match.groups()

    def _wrap(self, item: objectify.ObjectifiedDataElement) -> ElementType:
        """Make sure that a returned item is wrapped correctly to support further navigation"""
        if item.text is not None:
            # We have a primitive type value
            return item.pyval

        return ObjectElement(item)

    def __getattr__(self, name: str) -> ElementType:
        """Get a child of this element. When an underscore is provided and the lookup fails a lookup
        with - will be done.
        """
        ele = self.get_subelement(name)
        if ele is None:
            if "_" in name:
                return self.__getattr__(name.replace("_", "-"))
            else:
                raise AttributeError(
                    f"Element {repr(self._object)} does not have a child {name}"
                )

        return ele

    def __getitem__(self, key: Union[int, str]) -> ElementType:
        """Support using object[something]. When a string is provided a child element lookup is performed. When
        a number is provided a list lookup is performed.
        """
        if isinstance(key, int):
            return self._wrap(self._object.getchildren()[key])

        return self.__getattr__(key)

    def __iter__(self) -> Iterator[ElementType]:
        """Returns a generator to loop over the children (if any)"""
        return (self._wrap(x) for x in self._object.getchildren())

    def get_subelement(self, name: str, namespace: Optional[str] = None) -> ElementType:
        """
        Search for a subelement in the children of this element. If the provided name is unique it will
        return it, even if no namespace is provided.

        :param name: The name of the child element
        :param namespace: The namespace of the child element
        """
        children: List[objectify.ObjectifiedDataElement] = self._object.getchildren()
        selected: List[objectify.ObjectifiedDataElement] = []
        for child in children:
            tag_match = self.TAG_REGEX.match(child.tag)
            if not tag_match:
                LOGGER.warning(
                    f"The following tag didn't match the expected format: {child.tag}.  "
                    "It will be skipped."
                )
                continue

            child_namespace, child_name = tag_match.groups()

            if name != child_name:
                # The name doesn't match
                continue

            if not namespace:
                # The name matches and no namespace is provided
                selected.append(child)
                continue

            if namespace == child_namespace:
                # The name and the namespace both are a match
                selected.append(child)

        if len(selected) > 1:
            raise Exception(
                f"Found multiple elements with similar tags: {[s.tag for s in selected]}"
            )

        if not selected:
            return None

        return self._wrap(selected[0])

    def __repr__(self) -> str:
        return f"Object>{repr(self._object)}"

    def to_tree(self) -> str:
        return etree.tostring(self._object, pretty_print=True).decode()

    @property
    def attributes(self) -> AttributeItem:
        return AttributeItem(self._object)

    @property
    def relations(self) -> RelationItem:
        return RelationItem(self._object)

    @property
    def list_attributes(self) -> AttributeList:
        return AttributeList(self._object)

    @property
    def list_relations(self) -> RelationList:
        return RelationList(self._object)
